from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from model.materia_model import cadastrar_materia, buscar_materias
from model.trabalho_model import cadastrar_trabalho, buscar_trabalhos, buscar_trabalho_por_id, atualizar_trabalho, desativar_trabalho

materia_bp = Blueprint('materia', __name__)

# US11: trabalhos com prazo em até N dias (e ainda não concluídos) ganham destaque
DIAS_ALERTA = 3

def calcular_destaques(trabalhos):
    """Retorna {id_do_trabalho: dias_restantes} para os trabalhos que merecem destaque.
    dias_restantes < 0 significa prazo vencido; 0 = vence hoje."""
    hoje = datetime.now().date()
    destaques = {}
    for t in trabalhos:
        if t[5] == 'Concluído':
            continue
        dias = (datetime.strptime(t[3], '%Y-%m-%d').date() - hoje).days
        if dias <= DIAS_ALERTA:
            destaques[t[0]] = dias
    return destaques

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
            nota = request.form.get('nota')
            
            data_prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
            hoje = datetime.now().date()
            
            if status != 'Concluído':
                if data_prazo < hoje:
                    status = 'Atrasado'
                elif data_prazo == hoje:
                    prioridade = 'Alta'
            
            nota_val = float(nota) if nota else None
            cadastrar_trabalho(descricao, materia_id, prazo, prioridade, status, nota_val)
            
        return redirect(url_for('materia.home'))
    
    filtro_materia = request.args.get('materia_id')
    filtro_prioridade = request.args.get('prioridade')
    filtro_status = request.args.get('status')
    termo_busca = request.args.get('busca')
    ordem = request.args.get('ordem', 'asc')
    if ordem not in ('asc', 'desc'):
        ordem = 'asc'
    apenas_concluidos = request.args.get('apenas_concluidos') == '1'
    
    materias_salvas = buscar_materias()
    
    trabalhos_salvos = buscar_trabalhos(
        materia_id=filtro_materia, 
        prioridade=filtro_prioridade, 
        status=filtro_status, 
        busca=termo_busca,
        apenas_concluidos=apenas_concluidos,
        ordem=ordem
    )
    
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

    # --- Cálculo de Médias Finais e Critérios de Aprovação ---
    medias_materias = {}
    for materia in materias_salvas:
        m_id, m_nome = materia[0], materia[1]
        # t[2] é o nome da matéria, t[7] é a nota
        trabalhos_materia = [t for t in todos_trabalhos if t[2] == m_nome and t[7] is not None]
        
        if trabalhos_materia:
            soma_notas = sum(t[7] for t in trabalhos_materia)
            media = soma_notas / len(trabalhos_materia)
            status_aprovacao = "Aprovado" if media >= 6.0 else "Reprovado"
        else:
            media = 0.0
            status_aprovacao = "Sem notas"
            
        medias_materias[m_id] = {
            'media': round(media, 2),
            'situacao': status_aprovacao
        }
    # ---------------------------------------------------------------

    return render_template('index.html', 
                           materias=materias_salvas, 
                           trabalhos=trabalhos_salvos,
                           totais=totais,
                           medias_materias=medias_materias,
                           destaques=calcular_destaques(trabalhos_salvos))

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
        nota = request.form.get('nota')
        
        data_prazo = datetime.strptime(prazo, '%Y-%m-%d').date()
        hoje = datetime.now().date()
        
        if status != 'Concluído':
            if data_prazo < hoje:
                status = 'Atrasado'
            elif data_prazo == hoje:
                prioridade = 'Alta'
        
        nota_val = float(nota) if nota else None
        atualizar_trabalho(trabalho_id, descricao, materia_id, prazo, prioridade, status, nota_val)
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
                           totais=totais,
                           destaques=calcular_destaques(todos_trabalhos))

@materia_bp.route('/trabalho/<int:trabalho_id>/desativar')
def desativar(trabalho_id):
    desativar_trabalho(trabalho_id)
    return redirect(url_for('materia.home'))