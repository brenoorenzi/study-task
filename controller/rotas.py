from flask import Blueprint, render_template, request, redirect, url_for
from model.materia_model import cadastrar_materia, buscar_materias

materia_bp = Blueprint('materia', __name__)

@materia_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nome = request.form['nome']
        cadastrar_materia(nome)
        return redirect(url_for('materia.home'))
    
    materias_salvas = buscar_materias()
    return render_template('index.html', materias=materias_salvas)