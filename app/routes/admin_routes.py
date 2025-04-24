from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.database import fetch_all, execute_query
from app.utils.decorators import require_level

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/painel_admin')
@require_level(3)  # Apenas nível 3 ou 4
def painel_admin():
    if not 'usuario' in session:
        return redirect(url_for('auth.home'))
    query_users = "SELECT id, nome, nivel FROM usuarios"
    usuarios = fetch_all(query_users, ())
    
    query_logs = "SELECT usuario, data_hora FROM logs ORDER BY id DESC LIMIT 20"
    logs = fetch_all(query_logs, ())
    
    query_tentatives = "SELECT usuario_tentado, data_hora, ip, sucesso FROM tentativas_login ORDER BY id DESC LIMIT 20"
    tentativas = fetch_all(query_tentatives, ())
 
    return render_template('painel_admin.html', usuarios=usuarios, nivel_atual=session['nivel'], logs=logs, tentativas=tentativas)
   
@admin_bp.route('/excluir_usuario', methods=['POST'])
@require_level(3)
def excluir_usuario():
    id = request.form['id']
    try:
        int(id)
        query = "DELETE FROM usuarios WHERE id=?"
        execute_query(query, (id,))
        return redirect(url_for('admin.painel_admin'))
    except ValueError:
    	return "ID Invalido", 400

@admin_bp.route('/alterar_nivel', methods=['POST'])
@require_level(3)
def alterar_nivel():
    id = request.form['id']
    novo_nivel = request.form['nivel']
    query = "UPDATE usuarios SET nivel=? WHERE id=?"
    execute_query(query, (novo_nivel, id))
    return redirect(url_for('admin.painel_admin'))

@admin_bp.route('/show_db')
@require_level(4)
def show_db():

    # Pega dados de todas as tabelas
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    tabelas = fetch_all(query, ())

    dados = {}
    for tabela in tabelas:
        tabela = tabela[0]
        sel_query = f"SELECT * FROM {tabela}"
        dados[tabela] = fetch_all(sel_query, ())
    return render_template('ver_db.html', dados=dados)

