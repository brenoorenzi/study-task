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
            ativo INTEGER DEFAULT 1,
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

def buscar_trabalhos(materia_id=None, prioridade=None, status=None, busca=None):
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    query = '''
        SELECT t.id, t.descricao, m.nome, t.prazo, t.prioridade, t.status, m.id 
        FROM trabalhos t
        JOIN materias m ON t.materia_id = m.id
        WHERE t.ativo = 1
    '''
    parametros = []
    
    if materia_id:
        query += ' AND t.materia_id = ?'
        parametros.append(materia_id)
        
    if prioridade:
        query += ' AND t.prioridade = ?'
        parametros.append(prioridade)
        
    if status:
        query += ' AND t.status = ?'
        parametros.append(status)
        
    if busca:
        query += ' AND t.descricao LIKE ?'
        parametros.append(f'%{busca}%')
        
    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def buscar_trabalho_por_id(trabalho_id):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT id, descricao, materia_id, prazo, prioridade, status
        FROM trabalhos
        WHERE id = ? AND ativo = 1
    ''', (trabalho_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def atualizar_trabalho(trabalho_id, descricao, materia_id, prazo, prioridade, status):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE trabalhos
        SET descricao = ?, materia_id = ?, prazo = ?, prioridade = ?, status = ?
        WHERE id = ?
    ''', (descricao, materia_id, prazo, prioridade, status, trabalho_id))
    conexao.commit()
    conexao.close()

def desativar_trabalho(trabalho_id):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('UPDATE trabalhos SET ativo = 0 WHERE id = ?', (trabalho_id,))
    conexao.commit()
    conexao.close()