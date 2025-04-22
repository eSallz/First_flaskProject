import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Apagar a tabela usuarios
cursor.execute("DROP TABLE IF EXISTS usuarios;CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE, senha TEXT NOT NULL, pergunta TEXT NOT NULL,resposta TEXT NOT NULL, nivel INTEGER DEFAULT 0)")

conn.commit()
conn.close()

print("Tabela 'usuarios' apagada com sucesso.")