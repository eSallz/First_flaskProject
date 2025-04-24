from flask import Flask
from app.models import init_db

def create_app():
	app = Flask(__name__)
	app.secret_key = '1532_ab@'
	
	init_db()
	
	from app.routes import init_app
	from app.handlers.error_handles import init_error_handles as ieh
	init_app(app)
	ieh(app)
	return app
	
