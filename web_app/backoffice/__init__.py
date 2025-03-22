import os
import requests

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
        return render_template('index.html')
    
    base_api_url = 'http://localhost:5001/api'
    
    # Rotas da aplicação
    # usuários
    @app.route('/usuarios', methods=['GET'])
    def usuarios():
        usuarios = getUsuarios()
        return render_template('usuarios/index.html', usuarios=usuarios)
    
    @app.route('/usuarios/novo', methods=['GET', 'POST'])
    def novo_usuario():
        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/usuarios/create'

            requests.post(api_url, json={
                'name': data['name'],
                'email': data['email'],
                'role': 'user',
                'is_activated': 1 if data['is_activated'] == 'true' else 0,
                'phone': data['phone'],
                'cpf': data['cpf']
            })
            return redirect(url_for('usuarios'))
        
        return render_template('usuarios/create.html')
    
    @app.route('/usuarios/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        usuario = getUsuario(id)

        if request.method == 'POST':
            data = request.form
            print(data)
            api_url = base_api_url + '/usuarios/update/' + str(id)

            requests.put(api_url, json={
                'name': data['name'],
                'email': data['email'],
                'role': 'user',
                'is_activated': 1 if data['is_activated'] == 'true' else 0,
                'phone': data['phone'],
                'cpf': data['cpf']
            })
            return redirect(url_for('usuarios'))
        
        return render_template('usuarios/edit.html', usuario=usuario)
    
    @app.route('/usuarios/delete/<int:id>', methods=['GET'])
    def delete_usuario(id):
        requests.delete(base_api_url + '/usuarios/delete/' + str(id))
        return redirect(url_for('usuarios'))
    
    def getUsuarios():
        return requests.get(base_api_url + '/usuarios').json()
    
    def getUsuario(id):
        return requests.get(base_api_url + '/usuarios/' + str(id)).json()
    
    # livros
    @app.route('/livros', methods=['GET'])
    def livros():
        livros = getLivros()
        return render_template('livros/index.html', livros=livros)
    
    @app.route('/livros/novo', methods=['GET', 'POST'])
    def novo_livro():
        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/livros/create'

            requests.post(api_url, json={
                'title': data['title'],
                'autor': data['author'],
                'editor': data['editor'],
                'publish_year': data['publish_year'],
                'isbn': data['isbn'],
                'category': data['category'],
                'localization': data['localization'],
                'is_activated': 1
            })
            return redirect(url_for('livros'))
        
        return render_template('livros/create.html')
    
    @app.route('/livros/<int:id>', methods=['GET', 'POST'])
    def editar_livro(id):
        livro = getLivro(id)

        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/livros/update/' + str(id)

            requests.put(api_url, json={
                'title': data['title'],
                'autor': data['author'],
                'editor': data['editor'],
                'publish_year': data['publish_year'],
                'isbn': data['isbn'],
                'category': data['category'],
                'localization': data['localization'],
                'is_activated': 1
            })
            return redirect(url_for('livros'))
        
        return render_template('livros/edit.html', livro=livro)
    
    @app.route('/livros/delete/<int:id>', methods=['GET'])
    def delete_livro(id):
        requests.delete(base_api_url + '/livros/delete/' + str(id))
        return redirect(url_for('livros'))
    
    def getLivros():
        return requests.get('http://localhost:5001/api/livros').json()
    
    def getLivro(id):
        return requests.get(base_api_url + '/livros/' + str(id)).json()

    # empréstimos
    @app.route('/emprestimos', methods=['GET'])
    def emprestimos():
        emprestimos = getEmprestimos()
        return render_template('emprestimos/index.html', emprestimos=emprestimos)
    
    @app.route('/emprestimos/novo', methods=['GET', 'POST'])
    def novo_emprestimo():
        usuarios = getUsuarios()
        livros = getLivros()

        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/emprestimos/create'

            requests.post(api_url, json={
                'book_id': data['book_id'],
                'user_id': data['user_id'],
                'loan_date': data['loan_date'],
                'return_date': data['return_date'],
                'is_activated': 1 if data['is_activated'] == 'true' else 0
            })
            return redirect(url_for('emprestimos'))
        
        return render_template('emprestimos/create.html', usuarios=usuarios, livros=livros)
    
    @app.route('/emprestimos/<int:id>', methods=['GET', 'POST'])
    def editar_emprestimo(id):
        emprestimo = getEmprestimo(id)
        usuarios = getUsuarios()
        livros = getLivros()

        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/emprestimos/update/' + str(id)

            requests.put(api_url, json={
                'book_id': data['book_id'],
                'user_id': data['user_id'],
                'loan_date': data['loan_date'],
                'return_date': data['return_date'],
                'is_activated': 1 if data['is_activated'] == 'true' else 0
            })
            return redirect(url_for('emprestimos'))
        
        return render_template('emprestimos/edit.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
    
    @app.route('/emprestimos/delete/<int:id>', methods=['GET'])
    def delete_emprestimo(id):
        requests.delete(base_api_url + '/emprestimos/delete/' + str(id))
        return redirect(url_for('emprestimos'))
    
    def getEmprestimos():
        return requests.get(base_api_url + '/emprestimos').json()
    
    def getEmprestimo(id):
        return requests.get(base_api_url + '/emprestimos/' + str(id)).json()
    
    def date_filter(d):
        d = datetime.strptime(d, "%Y-%m-%d")
        return d.strftime('%d/%m/%Y')
    
    app.add_template_filter(date_filter)

    return app