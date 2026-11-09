from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from model.materia_model import cadastrar_materia, buscar_materias
from model.trabalho_model import cadastrar_trabalho, buscar_trabalhos, buscar_trabalho_por_id, atualizar_trabalho, desativar_trabalho

materia_bp = Blueprint('materia', __name__)

@materia_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'nome_materia' in request.form:
            nome = request.form['nome_materia']
            cadastrar_materia(nome)
        
        elif 'descricao_trabalho' in request.form:
            descricao = request.form['descricao_trabalho']
            materia_id = request.form['materia_id']
            prazo = request.form['prazo']
            prioridade = request.form['prioridade']
            status = request.form['status']
            
            data_prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            
            if status != 'Concluído':
                if data_prazo < hoje:
                    status = 'Atrasado'
                elif data_prazo == hoje:
                    prioridade = 'Alta'
            
            cadastrar_trabalho(descricao, materia_id, prazo, prioridade, status)
            
        return redirect(url_for('materia.home'))
    
    # Capturando parâmetros de filtro e busca via GET
    filtro_materia = request.args.get('materia_id')
    filtro_prioridade = request.args.get('prioridade')
    filtro_status = request.args.get('status')
    termo_busca = request.args.get('busca')
    
    materias_salvas = buscar_materias()
    
    # Busca filtrada para a listagem
    trabalhos_salvos = buscar_trabalhos(
        materia_id=filtro_materia, 
        prioridade=filtro_prioridade, 
        status=filtro_status, 
        busca=termo_busca
    )
    
    # Para o painel de totais, buscamos todos os trabalhos sem filtros para manter as estatísticas globais corretas
    todos_trabalhos = buscar_trabalhos()
    total_geral = len(todos_trabalhos)
    total_concluidos = sum(1 for t in todos_trabalhos if t[5] == 'Concluído')
    total_pendentes = sum(1 for t in todos_trabalhos if t[5] in ['Pendente', 'Fazendo'])
    total_atrasados = sum(1 for t in todos_trabalhos if t[5] == 'Atrasado')
    
    totais = {
        'geral': total_geral,
        'concluidos': total_concluidos,
        'pendentes': total_pendentes,
        'atrasados': total_atrasados
    }

    return render_template('index.html', 
                           materias=materias_salvas, 
                           trabalhos=trabalhos_salvos,
                           totais=totais)

@materia_bp.route('/trabalho/<int:trabalho_id>/editar', methods=['GET', 'POST'])
def editar_trabalho(trabalho_id):
    trabalho = buscar_trabalho_por_id(trabalho_id)
    if trabalho is None:
        return redirect(url_for('materia.home'))

    if request.method == 'POST':
        descricao = request.form['descricao_trabalho']
        materia_id = request.form['materia_id']
        prazo = request.form['prazo']
        prioridade = request.form['prioridade']
        status = request.form['status']
        
        data_prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
        hoje = datetime.now().date()
        
        if status != 'Concluído':
            if data_prazo < hoje:
                status = 'Atrasado'
            elif data_prazo == hoje:
                prioridade = 'Alta'
        
        atualizar_trabalho(trabalho_id, descricao, materia_id, prazo, prioridade, status)
        return redirect(url_for('materia.home'))

    materias_salvas = buscar_materias()
    todos_trabalhos = buscar_trabalhos()
    
    total_geral = len(todos_trabalhos)
    total_concluidos = sum(1 for t in todos_trabalhos if t[5] == 'Concluído')
    total_pendentes = sum(1 for t in todos_trabalhos if t[5] in ['Pendente', 'Fazendo'])
    total_atrasados = sum(1 for t in todos_trabalhos if t[5] == 'Atrasado')
    
    totais = {
        'geral': total_geral,
        'concluidos': total_concluidos,
        'pendentes': total_pendentes,
        'atrasados': total_atrasados
    }

    return render_template('index.html',
                           materias=materias_salvas,
                           trabalhos=todos_trabalhos,
                           trabalho_edicao=trabalho,
                           totais=totais)

@materia_bp.route('/trabalho/<int:trabalho_id>/desativar')
def desativar(trabalho_id):
    desativar_trabalho(trabalho_id)
    return redirect(url_for('materia.home'))