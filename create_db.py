import sqlite3

# Cria novo banco ou abre se já existir
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Cria a tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print('Banco e tabela criados com sucesso!')