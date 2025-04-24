from flask import Blueprint, render_template, session, url_for, redirect
from app.utils.decorators import require_level

user_bp = Blueprint('user', __name__)

@user_bp.route('/painel')
@require_level(1)
def painel():
	if not 'usuario' in session:
		return redirect (url_for('auth.home'))
		
	return render_template('painel.html', usuario=session['usuario'], nivel=session['nivel'])
		