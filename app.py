from flask import Flask
from controller.rotas import materia_bp
from model.materia_model import criar_tabela

app = Flask(__name__)
app.register_blueprint(materia_bp)

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)