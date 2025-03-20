import os
import requests

from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def index():
        return 'Salve rapeize!!'
    
    # Rotas da aplicação
    # usuários
    @app.route('/usuarios', methods=['GET'])
    def usuarios():
        usuarios = getUsuarios()
        return render_template('usuarios/index.html', usuarios=usuarios)
    
    @app.route('/usuarios/novo', methods=['GET'])
    def novo_usuario():
        return render_template('usuarios/create.html')
    
    @app.route('/usuarios/<int:id>', methods=['GET'])
    def editar_usuario(id):
        usuario = getUsuario(id)
        return render_template('usuarios/edit.html', usuario=usuario)
    
    def getUsuarios():
        return requests.get('http://localhost:5001/api/usuarios').json()
    
    def getUsuario(id):
        return requests.get('http://localhost:5001/api/usuarios/' + str(id)).json()
    
    # livros
    @app.route('/livros', methods=['GET'])
    def livros():
        livros = getLivros()
        return render_template('livros/index.html', livros=livros)
    
    @app.route('/livros/novo', methods=['GET'])
    def novo_livro():
        return render_template('livros/create.html')
    
    @app.route('/livros/<int:id>', methods=['GET'])
    def editar_livro(id):
        livro = getLivro(id)
        return render_template('livros/edit.html', livro=livro)
    
    def getLivros():
        return requests.get('http://localhost:5001/api/livros').json()
    
    def getLivro(id):
        return requests.get('http://localhost:5001/api/livros/' + str(id)).json()

    # empréstimos
    @app.route('/emprestimos', methods=['GET'])
    def emprestimos():
        emprestimos = getEmprestimos()
        return render_template('emprestimos/index.html', emprestimos=emprestimos)
    
    @app.route('/emprestimos/novo', methods=['GET'])
    def novo_emprestimo():
        return render_template('emprestimos/create.html')
    
    @app.route('/emprestimos/<int:id>', methods=['GET'])
    def editar_emprestimo(id):
        emprestimo = getEmprestimo(id)
        return render_template('emprestimos/edit.html', emprestimo=emprestimo)
    
    def getEmprestimos():
        return requests.get('http://localhost:5001/api/emprestimos').json()
    
    def getEmprestimo(id):
        return requests.get('http://localhost:5001/api/emprestimos/' + str(id)).json()

    return app