import sqlite3

def get_conexao():
    return sqlite3.connect('banco.db')

def criar_tabela_trabalhos():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trabalhos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            materia_id INTEGER NOT NULL,
            prazo TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        )
    ''')
    conexao.commit()
    conexao.close()

def cadastrar_trabalho(descricao, materia_id, prazo, prioridade, status):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO trabalhos (descricao, materia_id, prazo, prioridade, status) 
        VALUES (?, ?, ?, ?, ?)
    ''', (descricao, materia_id, prazo, prioridade, status))
    conexao.commit()
    conexao.close()

def buscar_trabalhos():
    conexao = get_conexao()
    cursor = conexao.cursor()
    # Usamos JOIN para buscar o nome da matéria vinculada ao trabalho
    cursor.execute('''
        SELECT t.id, t.descricao, m.nome, t.prazo, t.prioridade, t.status 
        FROM trabalhos t
        JOIN materias m ON t.materia_id = m.id
    ''')
    resultado = cursor.fetchall()
    conexao.close()
    return resultado