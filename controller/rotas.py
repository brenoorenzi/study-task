from flask import Blueprint, render_template, request, redirect, url_for
from model.materia_model import cadastrar_materia, buscar_materias
from model.trabalho_model import cadastrar_trabalho, buscar_trabalhos

materia_bp = Blueprint('materia', __name__)

@materia_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Verifica se é o formulário de matéria
        if 'nome_materia' in request.form:
            nome = request.form['nome_materia']
            cadastrar_materia(nome)
        
        # Verifica se é o formulário de trabalho
        elif 'descricao_trabalho' in request.form:
            descricao = request.form['descricao_trabalho']
            materia_id = request.form['materia_id']
            prazo = request.form['prazo']
            prioridade = request.form['prioridade']
            status = request.form['status']
            cadastrar_trabalho(descricao, materia_id, prazo, prioridade, status)
            
        return redirect(url_for('materia.home'))
    
    # Renderiza a página com dados de ambas as tabelas
    materias_salvas = buscar_materias()
    trabalhos_salvos = buscar_trabalhos()
    return render_template('index.html', materias=materias_salvas, trabalhos=trabalhos_salvos)