from flask import Flask
from controller.rotas import materia_bp
from model.materia_model import criar_tabela
from model.trabalho_model import criar_tabela_trabalhos

app = Flask(__name__)
app.register_blueprint(materia_bp)

if __name__ == '__main__':
    criar_tabela()
    criar_tabela_trabalhos() # Cria a tabela de trabalhos se não existir
    app.run(debug=True)