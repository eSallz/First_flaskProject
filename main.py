from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort
from datetime import datetime

NIVEIS = {
    'comum': 1,
    'moderador': 2,
    'admin': 3,
    'master': 4
}

def require_level(nivel_requerido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'nivel' not in session or NIVEIS.get(session['nivel'], 0) < nivel_requerido:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


app = Flask(__name__)
app.secret_key = '1532_ab@'

USER = "admin"
PWD = "admin123"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/home')
def start():
	return render_template('home.html')
	
def registrar_log(usuario):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO logs (usuario, data_hora) VALUES (?, ?)", (usuario, agora))
    conn.commit()
    conn.close()

def registrar_tentativa(usuario_tentado, sucesso):
    ip = request.remote_addr
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tentativas_login (usuario_tentado, data_hora, ip, sucesso)
        VALUES (?, ?, ?, ?)
    ''', (usuario_tentado, agora, ip, int(sucesso)))
    conn.commit()
    conn.close()
    
@app.route('/login', methods=['POST'])
def login():
    nome = request.form['usuario']
    senha = request.form['senha']
    
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha, nivel FROM usuarios WHERE nome=?", (nome,))
    user = cursor.fetchone()

    if user and check_password_hash(user[0], senha):
        session['usuario'] = nome
        session['nivel'] = user[1]
        registrar_log(nome)
        registrar_tentativa(nome, True)
        return redirect(url_for('painel'))
    else:
        registrar_tentativa(nome, False)
        return render_template('mensagens.html',
            titulo="Erro no Login",
            mensagem="Usuário ou senha incorretos. Tente novamente.",
            url=url_for('home'),
            texto_botao='Início')

@app.route('/painel')
@require_level(0)
def painel():
	if 'usuario' in session:
		return render_template('painel.html', usuario=session['usuario'], nivel=session['nivel'])
	else:
		return redirect (url_for('home'))
		
@app.route('/painel_admin')
@require_level(3)  # Apenas nível 3 ou 4
def painel_admin():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, nivel FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.execute("SELECT usuario, data_hora FROM logs ORDER BY id DESC LIMIT 20")
    logs = cursor.fetchall()
    cursor.execute("SELECT usuario_tentado, data_hora, ip, sucesso FROM tentativas_login ORDER BY id DESC LIMIT 20")
    tentativas = cursor.fetchall()
    conn.close()
    return render_template('painel_admin.html', usuarios=usuarios, nivel_atual=session['nivel'], logs=logs, tentativas=tentativas)
   
@app.route('/excluir_usuario', methods=['POST'])
@require_level(3)
def excluir_usuario():
    id = request.form['id']
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('painel_admin'))

@app.route('/alterar_nivel', methods=['POST'])
@require_level(3)
def alterar_nivel():
    id = request.form['id']
    novo_nivel = request.form['nivel']
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nivel=? WHERE id=?", (novo_nivel, id))
    conn.commit()
    conn.close()
    return redirect(url_for('painel_admin'))
		
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))
    
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
    
@app.route('/salvar', methods=['POST'])
def salvar_usuario():
    nome = request.form['nome']
    senha = request.form['senha']
    pergunta = request.form['pergunta']
    resposta = request.form['resposta']

    if not nome or not senha or not pergunta or not resposta:
        return render_template('mensagens.html',
            titulo="Erro no Cadastro",
            mensagem="Todos os campos são obrigatórios.",
            url=url_for('cadastro'),
            texto_botao="Voltar")

    senha_hash = generate_password_hash(senha)
    resposta_hash = generate_password_hash(resposta)

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, senha, pergunta, resposta, nivel) VALUES (?, ?, ?, ?, ?)",
        (nome, senha_hash, pergunta, resposta_hash, 'master')
    )
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/perfil')
def perfil():
	if 'usuario' in session:
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute("SELECT id, nome FROM usuarios WHERE nome = ?", (session['usuario'],))
		user = cursor.fetchone()
		conn.close()
		if user:
			return render_template('perfil.html',
usuario=user)
	return redirect(url_for('home'))
	
@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():
	user_id = request.form['id']
	novo_nome = request.form['nome']
	nova_senha = request.form['senha']
	
	if novo_nome and nova_senha:
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute("UPDATE usuarios SET nome=?, senha=? WHERE id=?", (novo_nome, nova_senha, user_id))
		conn.commit()
		conn.close()
		session['usuario'] = novo_nome
		return redirect(url_for('painel'))
	return render_template('mensagens.html', titulo='Erro ao Salvar', mensagem='Erro ao atualizar perfil', url=url_for('painel'),
	texto_botao='Voltar')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        nome = request.form['usuario']
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT pergunta FROM usuarios WHERE nome = ?", (nome,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('responder.html', usuario=nome, pergunta=user[0])
        else:
            return render_template('mensagens.html',
                titulo="Erro",
                mensagem="Usuário não encontrado.",
                url=url_for('recuperar'),
                texto_botao="Tentar novamente")
    return render_template('recuperar.html')
    
@app.route('/verificar_resposta', methods=['POST'])
def verificar_resposta():
	nome = request.form['usuario']
	resposta = request.form['answer']
	nova_senha = request.form['nova_senha']
	conn = sqlite3.connect('usuarios.db')
	cursor = conn.cursor()
	cursor.execute("SELECT resposta FROM usuarios WHERE nome = ?", (nome,))
	user =cursor.fetchone()
	if user and check_password_hash(user[0], resposta):
		nova_hash = generate_password_hash(nova_senha)
		cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_hash, nome))
		conn.commit()
		msg = "Senha atualizada"
	else:
		msg = "Resposta incorreta"
	conn.close()
	return render_template('mensagens.html',
	titulo='Status',
	mensagem=mensagem,
	url=url_for('home'),
	texto_botao='Voltar')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
	if request.method == 'POST':
		nome = request.form['nome']
		return f'''<h2>
		Salve, {nome.capitalize()}! Recebi seu input!</h2>'''
	return render_template('formulario.html')

@app.errorhandler(403)
def acesso_negado(e):
    return render_template('mensagens.html',
        titulo="Acesso Negado",
        mensagem="Você não tem permissão para acessar esta página.",
        url=url_for('painel'),
        texto_botao='Voltar'), 403
        
def criar_tabela_logs():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_tentativas():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tentativas_login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_tentado TEXT,
            data_hora TEXT,
            ip TEXT,
            sucesso INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/ver_db')
def ver_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Pega dados de todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    
    dados = {}
    for tabela in tabelas:
        tabela = tabela[0]
        cursor.execute(f"SELECT * FROM {tabela}")
        dados[tabela] = cursor.fetchall()
    
    conn.close()
    return render_template('ver_db.html', dados=dados)

# Chama essa função no início do app.py
criar_tabela_logs()
criar_tabela_tentativas()
        
if __name__ == '__main__':
    app.run(debug=True)