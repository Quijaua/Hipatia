import os
import requests

from flask import Flask, render_template, request, redirect, url_for, flash
from .database.models import db, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from datetime import datetime, timedelta

def create_app(test_config=None):
    load_dotenv()
    login_manager = LoginManager()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Por favor, faça o login para aceesar esta página'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
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

    base_api_url = 'http://localhost:5001/api'

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/login'

            response = requests.post(api_url, json={
                'email': data['email'],
                'password': data['password'],
                'remember': True if data.get('remember') else False
            })
            if response.status_code == 200:
                user = User.query.filter_by(email=data['email']).first()
                login_user(user, remember=data.get('remember'))
                return redirect(url_for('index'))
            else:
                flash('Email ou senha inválidos')

        return render_template('login/index.html')
    
    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # Rotas da aplicação
    # usuários
    @app.route('/usuarios', methods=['GET'])
    @login_required
    def usuarios():
        usuarios = getUsuarios()
        return render_template('usuarios/index.html', usuarios=usuarios)
    
    @app.route('/usuarios/novo', methods=['GET', 'POST'])
    @login_required
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
            flash('Usuário criado com sucesso')
            return redirect(url_for('usuarios'))
        
        return render_template('usuarios/create.html')
    
    @app.route('/usuarios/<int:id>', methods=['GET', 'POST'])
    @login_required
    def editar_usuario(id):
        usuario = getUsuario(id)

        if usuario.get('error'):
            flash(usuario.get('error'))
            return redirect(url_for('usuarios'))

        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/usuarios/update/' + str(id)

            requests.put(api_url, json={
                'name': data['name'],
                'email': data['email'],
                'role': 'user',
                'is_activated': 1 if data['is_activated'] == 'true' else 0,
                'phone': data['phone'],
                'cpf': data['cpf']
            })
            flash('Usuário atualizado com sucesso')
            return redirect(url_for('usuarios'))
        
        return render_template('usuarios/edit.html', usuario=usuario)
    
    @app.route('/usuarios/delete/<int:id>', methods=['GET'])
    @login_required
    def delete_usuario(id):
        requests.delete(base_api_url + '/usuarios/delete/' + str(id))
        flash('Usuário excluído com sucesso')
        return redirect(url_for('usuarios'))
    
    def getUsuarios():
        return requests.get(base_api_url + '/usuarios').json()
    
    def getUsuario(id):
        return requests.get(base_api_url + '/usuarios/' + str(id)).json()
    
    # livros
    @app.route('/livros', methods=['GET'])
    @login_required
    def livros():
        livros = getLivros()
        return render_template('livros/index.html', livros=livros)
    
    @app.route('/livros/novo', methods=['GET', 'POST'])
    @login_required
    def novo_livro():
        status = getLivrosStatus()

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
                'is_activated': 1,
            })
            flash('Livro criado com sucesso')
            return redirect(url_for('livros'))
        
        return render_template('livros/create.html', status=status)
    
    @app.route('/livros/<int:id>', methods=['GET', 'POST'])
    @login_required
    def editar_livro(id):
        livro = getLivro(id)
        status = getLivrosStatus()

        if livro.get('error'):
            flash(livro.get('error'))
            return redirect(url_for('livros'))

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
                'is_activated': 1,
                'status_id': data['status_id'],
            })
            flash('Livro atualizado com sucesso')
            return redirect(url_for('livros'))
        
        return render_template('livros/edit.html', livro=livro, status=status)
    
    @app.route('/livros/delete/<int:id>', methods=['GET'])
    @login_required
    def delete_livro(id):
        requests.delete(base_api_url + '/livros/delete/' + str(id))
        flash('Livro excluído com sucesso')
        return redirect(url_for('livros'))
    
    def getLivros():
        return requests.get('http://localhost:5001/api/livros').json()
    
    def getLivro(id):
        return requests.get(base_api_url + '/livros/' + str(id)).json()
    
    def getLivrosStatus():
        return requests.get(base_api_url + '/livros/status').json()

    # empréstimos
    @app.route('/emprestimos', methods=['GET'])
    @login_required
    def emprestimos():
        emprestimos = getEmprestimos()
        return render_template('emprestimos/index.html', emprestimos=emprestimos)
    
    @app.route('/emprestimos/novo', methods=['GET', 'POST'])
    @login_required
    def novo_emprestimo():
        usuarios = getUsuarios()
        livros = getLivros()
        loan_date = datetime.now().strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')

        if request.method == 'POST':
            data = request.form
            api_url = base_api_url + '/emprestimos/create'

            requests.post(api_url, json={
                'book_id': data['book_id'],
                'user_id': data['user_id'],
                'loan_date': data['loan_date'],
                'return_date': data['return_date'],
                'is_activated': 1
            })
            flash('Empréstimo criado com sucesso')
            return redirect(url_for('emprestimos'))
        
        return render_template('emprestimos/create.html', usuarios=usuarios, livros=livros, loan_date=loan_date, return_date=return_date)
    
    @app.route('/emprestimos/<int:id>', methods=['GET', 'POST'])
    @login_required
    def editar_emprestimo(id):
        emprestimo = getEmprestimo(id)
        usuarios = getUsuarios()
        livros = getLivros()

        if emprestimo.get('error'):
            flash(emprestimo.get('error'))
            return redirect(url_for('emprestimos'))

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
            flash('Empréstimo atualizado com sucesso')
            return redirect(url_for('emprestimos'))
        
        return render_template('emprestimos/edit.html', emprestimo=emprestimo, usuarios=usuarios, livros=livros)
    
    @app.route('/emprestimos/devolucao/<int:id>', methods=['GET'])
    @login_required
    def devolucao_emprestimo(id):
        requests.put(base_api_url + '/emprestimos/devolucao/' + str(id))
        flash('Empréstimo devolvido com sucesso')
        return redirect(url_for('emprestimos'))
    
    @app.route('/emprestimos/renovacao/<int:id>', methods=['GET'])
    @login_required
    def renovacao_emprestimo(id):
        requests.put(base_api_url + '/emprestimos/renovacao/' + str(id))
        flash('Empréstimo renovado com sucesso')
        return redirect(url_for('emprestimos'))
    
    @app.route('/emprestimos/delete/<int:id>', methods=['GET'])
    @login_required
    def delete_emprestimo(id):
        requests.delete(base_api_url + '/emprestimos/delete/' + str(id))
        flash('Empréstimo excluído com sucesso')
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