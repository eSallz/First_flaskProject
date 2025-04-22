import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Apagar a tabela usuarios
cursor.execute("DROP TABLE IF EXISTS usuarios")

conn.commit()
conn.close()

print("Tabela 'usuarios' apagada com sucesso.")