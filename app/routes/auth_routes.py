from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.database import fetch_one, execute_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


auth_bp = Blueprint('auth', __name__)

def registrar_log(usuario):
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO logs (usuario, data_hora) VALUES (?, ?)"
    execute_query(query, (usuario, agora))

def registrar_tentativa(usuario_tentado, sucesso):
    ip = request.remote_addr
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = '''
        INSERT INTO tentativas_login (usuario_tentado, data_hora, ip, sucesso)
        VALUES (?, ?, ?, ?)
    '''
    execute_query(query, (usuario_tentado, agora, ip, int(sucesso)))

@auth_bp.route('/')
def login_show():
	if 'usuario' in session:
		return redirect(url_for('auth.home'))
	else:
		return render_template('login.html')

@auth_bp.route('/sign-in')
def home():
    if 'usuario' in session:
        return redirect(url_for('user.painel'))
    else:
    	return redirect(url_for('auth.login_show'))
    	
@auth_bp.route('/login', methods=['POST'])
def login():
    nome = request.form['usuario']
    senha = request.form['senha']
    query = "SELECT senha, nivel FROM usuarios WHERE nome=?"
    user = fetch_one(query, (nome,))
    
    if user and check_password_hash(user['senha'], senha):
        session['usuario'] = nome
        session['nivel'] = user['nivel']
        registrar_log(nome)
        registrar_tentativa(nome, True)
        return redirect(url_for('user.painel'))
    else:
        registrar_tentativa(nome, False)
        return render_template('mensagens.html',
            titulo="Erro no Login",
            mensagem="Usuário ou senha incorretos. Tente novamente.",
            url=url_for('auth.home'),
            texto_botao='Início')
            
@auth_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
    
@auth_bp.route('/salvar', methods=['POST'])
def salvar_usuario():
    nome = request.form['nome']
    senha = request.form['senha']
    pergunta = request.form['pergunta']
    resposta = request.form['resposta']

    if not nome or not senha or not pergunta or not resposta:
        return render_template('mensagens.html',
            titulo="Erro no Cadastro",
            mensagem="Todos os campos são obrigatórios.",
            url=url_for('auth.cadastro'),
            texto_botao="Voltar")

    senha_hash = generate_password_hash(senha)
    resposta_hash = generate_password_hash(resposta)

    query = "INSERT INTO usuarios (nome, senha, pergunta, resposta, nivel) VALUES (?, ?, ?, ?, ?)"
    execute_query(query, (nome, senha_hash, pergunta, resposta_hash, 'master'))

    return redirect(url_for('auth.home'))