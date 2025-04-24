import sqlite3

DATABASE_NAME = 'usuarios.db'

def get_connection():
	conn = sqlite3.connect(DATABASE_NAME)
	conn.row_factory = sqlite3.Row
	return conn
	
def execute_query(query, params=()):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, params)
	conn.commit()
	conn.close()
	
def fetch_one(query, params=()):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, params)
	result = cursor.fetchone()
	conn.close()
	return result
	
def fetch_all(query, params=()):
	conn = get_connection()
	cursor = conn.cursor()
	cursor.execute(query, params)
	result = cursor.fetchall()
	conn.close()
	return result
	