def criar_tabela_logs():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Chama essa função no início do app.py
criar_tabela_logs()