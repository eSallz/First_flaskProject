from flask import Flask, abort, session
from functools import wraps

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