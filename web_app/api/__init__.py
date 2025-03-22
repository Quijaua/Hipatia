import os

from flask import Flask, request
from .database.models import db, User, Book, Loan


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3er45ty6@172.17.0.2:5432/hipatia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'hipatia.sqlite'),
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

    # Rotas da API
    # usuários
    @app.route('/api/usuarios', methods=['GET'])
    def getUsuarios():
        usuarios = User.query.all()

        return [
            {
                'id': usuario.id,
                'nome': usuario.name,
                'email': usuario.email,
                'role': usuario.role,
                'is_activated': usuario.is_activated,
                'phone': usuario.phone,
                'cpf': usuario.cpf
            } for usuario in usuarios
        ]
    
    @app.route('/api/usuarios/<int:id>', methods=['GET'])
    def getUsuario(id):
        usuario = User.query.filter_by(id=id).first()

        if usuario is None:
            return {'error': 'Usuário não encontrado'}, 404

        return {
            'id': usuario.id,
            'nome': usuario.name,
            'email': usuario.email,
            'role': usuario.role,
            'is_activated': usuario.is_activated,
            'phone': usuario.phone,
            'cpf': usuario.cpf
        }
    
    @app.route('/api/usuarios/create', methods=['POST'])
    def createUsuario():
        data = request.get_json()

        usuario = User(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            is_activated=data['is_activated'],
            phone=data['phone'],
            cpf=data['cpf']
        )
        db.session.add(usuario)
        db.session.commit()

        return {
            'id': usuario.id,
            'nome': usuario.name,
            'email': usuario.email,
            'role': usuario.role,
            'is_activated': usuario.is_activated,
            'phone': usuario.phone,
            'cpf': usuario.cpf
        }
    
    @app.route('/api/usuarios/update/<int:id>', methods=['PUT'])
    def updateUsuario(id):
        data = request.get_json()

        usuario = User.query.filter_by(id=id).first()

        if usuario is None:
            return {'error': 'Usuário não encontrado'}, 404

        usuario.name = data['name']
        usuario.email = data['email']
        usuario.role = data['role']
        usuario.is_activated = data['is_activated']
        usuario.phone = data['phone']
        usuario.cpf = data['cpf']
        usuario.is_activated = data['is_activated']

        db.session.commit()

        return {
            'id': usuario.id,
            'nome': usuario.name,
            'email': usuario.email,
            'role': usuario.role,
            'is_activated': usuario.is_activated,
            'phone': usuario.phone,
            'cpf': usuario.cpf,
            'is_activated': usuario.is_activated
        }
    
    @app.route('/api/usuarios/delete/<int:id>', methods=['DELETE'])
    def deleteUsuario(id):
        usuario = User.query.filter_by(id=id).first()

        if usuario is None:
            return {'error': 'Usuário não encontrado'}, 404

        db.session.delete(usuario)
        db.session.commit()

        return {'message': 'Usuário deletado com sucesso'}
    
    # empréstimos
    @app.route('/api/emprestimos', methods=['GET'])
    def getEmprestimos():
        emprestimos = Loan.query.all()

        return [
            {
                'id': emprestimo.id,
                'book_id': emprestimo.book_id,
                'user_id': emprestimo.user_id,
                'loan_date': emprestimo.loan_date.strftime('%Y-%m-%d'),
                'return_date': emprestimo.return_date.strftime('%Y-%m-%d'),
                'is_activated': emprestimo.is_activated,
                'created_at': emprestimo.created_at,
                'book_id': emprestimo.book.id,
                'book_title': emprestimo.book.title,
                'user_id': emprestimo.user.id,
                'user_name': emprestimo.user.name

            } for emprestimo in emprestimos
        ]
    
    @app.route('/api/emprestimos/<int:id>', methods=['GET'])
    def getEmprestimo(id):
        emprestimo = Loan.query.filter_by(id=id).first()

        if emprestimo is None:
            return {'error': 'Empréstimo não encontrado'}, 404

        return {
            'id': emprestimo.id,
            'book_id': emprestimo.book_id,
            'user_id': emprestimo.user_id,
            'loan_date': emprestimo.loan_date.strftime('%Y-%m-%d'),
            'return_date': emprestimo.return_date.strftime('%Y-%m-%d'),
            'is_activated': emprestimo.is_activated,
            'created_at': emprestimo.created_at,
            'book_id': emprestimo.book.id,
            'book_title': emprestimo.book.title,
            'user_id': emprestimo.user.id,
            'user_name': emprestimo.user.name
        }
    
    @app.route('/api/emprestimos/create', methods=['POST'])
    def createEmprestimo():
        data = request.get_json()

        emprestimo = Loan(
            book_id=data['book_id'],
            user_id=data['user_id'],
            loan_date=data['loan_date'],
            return_date=data['return_date'],
            is_activated=data['is_activated']
        )
        db.session.add(emprestimo)
        db.session.commit()

        return {
            'id': emprestimo.id,
            'livro': emprestimo.book_id,
            'usuario': emprestimo.user_id,
            'emprestado_em': emprestimo.loan_date,
            'devolvido_em': emprestimo.return_date,
            'is_activated': emprestimo.is_activated,
            'created_at': emprestimo.created_at
    }

    @app.route('/api/emprestimos/update/<int:id>', methods=['PUT'])
    def updateEmprestimo(id):
        data = request.get_json()

        emprestimo = Loan.query.filter_by(id=id).first()

        if emprestimo is None:
            return {'error': 'Empréstimo não encontrado'}, 404

        emprestimo.book_id = data['book_id']
        emprestimo.user_id = data['user_id']
        emprestimo.loan_date = data['loan_date']
        emprestimo.return_date = data['return_date']
        emprestimo.is_activated = data['is_activated']

        db.session.commit()

        return {
            'id': emprestimo.id,
            'livro': emprestimo.book_id,
            'usuario': emprestimo.user_id,
            'emprestado_em': emprestimo.loan_date,
            'devolvido_em': emprestimo.return_date,
            'is_activated': emprestimo.is_activated,
            'created_at': emprestimo.created_at
        }
    
    @app.route('/api/emprestimos/delete/<int:id>', methods=['DELETE'])
    def deleteEmprestimo(id):
        emprestimo = Loan.query.filter_by(id=id).first()

        if emprestimo is None:
            return {'error': 'Empréstimo não encontrado'}, 404

        db.session.delete(emprestimo)
        db.session.commit()

        return {'message': 'Empréstimo deletado com sucesso'}
    
    # livros
    @app.route('/api/livros', methods=['GET'])
    def getLivros():
        livros = Book.query.all()

        return [
            {
                'id': livro.id,
                'title': livro.title,
                'autor': livro.autor,
                'editor': livro.editor,
                'publish_year': livro.publish_year,
                'isbn': livro.isbn,
                'category': livro.category,
                'localization': livro.localization,
                'is_activated': livro.is_activated
            } for livro in livros
        ]
    
    @app.route('/api/livros/<int:id>', methods=['GET'])
    def getLivro(id):
        livro = Book.query.filter_by(id=id).first()

        if livro is None:
            return {'error': 'Livro não encontrado'}, 404

        return {
            'id': livro.id,
            'title': livro.title,
            'autor': livro.autor,
            'editor': livro.editor,
            'publish_year': livro.publish_year,
            'isbn': livro.isbn,
            'category': livro.category,
            'localization': livro.localization,
            'is_activated': livro.is_activated
        }
    
    @app.route('/api/livros/create', methods=['POST'])
    def createLivro():
        data = request.get_json()

        livro = Book(
            title=data['title'],
            autor=data['autor'],
            editor=data['editor'],
            publish_year=data['publish_year'],
            isbn=data['isbn'],
            category=data['category'],
            localization=data['localization'],
            is_activated=data['is_activated']
        )
        db.session.add(livro)
        db.session.commit()

        return {
            'id': livro.id,
            'titulo': livro.title,
            'autor': livro.autor,
            'editora': livro.editor,
            'ano': livro.publish_year,
            'isbn': livro.isbn,
            'categoria': livro.category,
            'localizacao': livro.localization,
            'is_activated': livro.is_activated
        }
    
    @app.route('/api/livros/update/<int:id>', methods=['PUT'])
    def updateLivro(id):
        data = request.get_json()

        livro = Book.query.filter_by(id=id).first()

        if livro is None:
            return {'error': 'Livro não encontrado'}, 404

        livro.title = data['title']
        livro.autor = data['autor']
        livro.editor = data['editor']
        livro.publish_year = data['publish_year']
        livro.isbn = data['isbn']
        livro.category = data['category']
        livro.localization = data['localization']
        livro.is_activated = data['is_activated']

        db.session.commit()

        return {
            'id': livro.id,
            'titulo': livro.title,
            'autor': livro.autor,
            'editora': livro.editor,
            'ano': livro.publish_year,
            'isbn': livro.isbn,
            'categoria': livro.category,
            'localizacao': livro.localization,
            'is_activated': livro.is_activated
        }
    
    @app.route('/api/livros/delete/<int:id>', methods=['DELETE'])
    def deleteLivro(id):
        livro = Book.query.filter_by(id=id).first()

        if livro is None:
            return {'error': 'Livro não encontrado'}, 404

        db.session.delete(livro)
        db.session.commit()

        return {'message': 'Livro deletado com sucesso'}

    return app