from app.models.database import execute_query

def init_db():
    # Tabela de usuários
    execute_query("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel TEXT NOT NULL
    )
    """)

    # Tabela de logs
    execute_query("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        data_hora TEXT NOT NULL
    )
    """)

    # Tabela de tentativas de login
    execute_query("""
    CREATE TABLE IF NOT EXISTS tentativas_login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_tentado TEXT NOT NULL,
        data_hora TEXT NOT NULL,
        ip TEXT,
        sucesso INTEGER
    )
    """)