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
            nota REAL,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        )
    ''')
    # Migração segura para adicionar a coluna nota caso a tabela já exista
    try:
        cursor.execute('ALTER TABLE trabalhos ADD COLUMN nota REAL')
    except sqlite3.OperationalError:
        pass
    conexao.commit()
    conexao.close()

def cadastrar_trabalho(descricao, materia_id, prazo, prioridade, status, nota=None):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO trabalhos (descricao, materia_id, prazo, prioridade, status, nota) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (descricao, materia_id, prazo, prioridade, status, nota))
    conexao.commit()
    conexao.close()

def buscar_trabalhos(materia_id=None, prioridade=None, status=None, busca=None, apenas_concluidos=False, ordem='asc'):
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    query = '''
        SELECT t.id, t.descricao, m.nome, t.prazo, t.prioridade, t.status, m.id, t.nota 
        FROM trabalhos t
        JOIN materias m ON t.materia_id = m.id
        WHERE t.ativo = 1
    '''
    parametros = []
    
    if apenas_concluidos:
        query += " AND t.status = 'Concluído'"
    
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
    
    # US09: ordenação por prazo (o prazo é salvo como YYYY-MM-DD, então ordena corretamente).
    # A direção vem de uma lista fixa, nunca direto do usuário, para evitar SQL injection.
    direcao = 'DESC' if ordem == 'desc' else 'ASC'
    query += f' ORDER BY t.prazo {direcao}, t.id ASC'
        
    cursor.execute(query, parametros)
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def buscar_trabalho_por_id(trabalho_id):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT id, descricao, materia_id, prazo, prioridade, status, nota
        FROM trabalhos
        WHERE id = ? AND ativo = 1
    ''', (trabalho_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def atualizar_trabalho(trabalho_id, descricao, materia_id, prazo, prioridade, status, nota=None):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE trabalhos
        SET descricao = ?, materia_id = ?, prazo = ?, prioridade = ?, status = ?, nota = ?
        WHERE id = ?
    ''', (descricao, materia_id, prazo, prioridade, status, nota, trabalho_id))
    conexao.commit()
    conexao.close()

def desativar_trabalho(trabalho_id):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('UPDATE trabalhos SET ativo = 0 WHERE id = ?', (trabalho_id,))
    conexao.commit()
    conexao.close()