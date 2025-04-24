from flask import render_template, url_for, Blueprint

errors_bp = Blueprint('error', __name__)

def init_error_handlers(app):
    @errors_bp.errorhandler(403)
    def acesso_negado(e):
        return render_template('mensagens.html',
            titulo="Acesso Negado",
            mensagem="Você não tem permissão para acessar esta página.",
            url=url_for('misc.home'),
            texto_botao='Voltar à Página Inicial'), 403

    @errors_bp.errorhandler(404)
    def pagina_nao_encontrada(e):
        return render_template('mensagens.html',
            titulo="Página Não Encontrada",
            mensagem="Ops! A página que você tentou acessar não existe.",
            url=url_for('misc.home'),
            texto_botao='Ir para Início'), 404

    @errors_bp.errorhandler(500)
    def erro_interno(e):
        return render_template('mensagens.html',
            titulo="Erro Interno",
            mensagem="Ocorreu um erro inesperado. Tente novamente mais tarde.",
            url=url_for('misc.home'),
            texto_botao='Voltar ao Início'), 500