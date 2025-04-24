from flask import Blueprint, render_template, session, url_for, redirect
from app.models.database import execute_query, fetch_one
from app.utils.decorators import require_level
from werkzeug.security import generate_password_hash

misc_bp = Blueprint('misc', __name__)

@misc_bp.route('/home')
def start():
	return render_template('home.html')
	
@misc_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('misc.home'))
    
@misc_bp.route('/perfil')
@require_level(1)
def perfil():
	if 'usuario' in session:
		query = "SELECT id, nome FROM usuarios WHERE nome = ?"
		user = fetch_one(query, (session['usuario'],))
		if user:
			return render_template('perfil.html',
usuario=user)
	return redirect(url_for('misc.home'))
	
@misc_bp.route('/editar_perfil', methods=['POST'])
@require_level(1)
def editar_perfil():
	user_id = request.form['id']
	novo_nome = request.form['nome']
	nova_senha = request.form['senha']
	
	if novo_nome and nova_senha:
		query = "UPDATE usuarios SET nome=?, senha=? WHERE id=?"
		hashed_password = generate_password_hash(nova_senha)
execute_query(query, (novo_nome, hashed_password, user_id))
		session['usuario'] = novo_nome
		return redirect(url_for('user.painel'))
	return render_template('mensagens.html', titulo='Erro ao Salvar', mensagem='Erro ao atualizar perfil', url=url_for('user.painel'),
	texto_botao='Voltar')