import sqlite3

def get_conexao():
    return sqlite3.connect('banco.db')

def criar_tabela():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def cadastrar_materia(nome):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO materias (nome) VALUES (?)', (nome,))
    conexao.commit()
    conexao.close()

def buscar_materias():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM materias')
    resultado = cursor.fetchall()
    conexao.close()
    return resultado