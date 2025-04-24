import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Adiciona a coluna 'nivel' se ainda não existir
try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN nivel TEXT DEFAULT 'comum'")
    print("Coluna 'nivel' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    print("Provavelmente a coluna já existe:", e)

conn.commit()
conn.close()