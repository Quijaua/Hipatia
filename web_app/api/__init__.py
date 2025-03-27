import os
import requests

from flask import Flask, request
from .database.models import db, User, Book, BookStatus, Loan
from dotenv import load_dotenv
from datetime import timedelta


def create_app(test_config=None):
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        if len(BookStatus.query.all()) == 0:
            db.session.add(BookStatus(name='Disponivel'))
            db.session.add(BookStatus(name='Emprestado'))
            db.session.add(BookStatus(name='Reservado'))
            db.session.add(BookStatus(name='Extraviado'))
            db.session.commit()

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

        return {'message': 'Usuário excluído com sucesso'}
    
    # empréstimos
    @app.route('/api/emprestimos', methods=['GET'])
    def getEmprestimos():
        emprestimos = Loan.query.where(Loan.is_activated == True).all()

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
                'book_isbn': emprestimo.book.isbn,
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

        book = Book.query.filter_by(id=data['book_id']).first()
        book.status_id = 2
        
        db.session.add(emprestimo, book)
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

        if emprestimo.is_activated == 0:
            book = Book.query.filter_by(id=data['book_id']).first()
            book.status_id = 1

        if emprestimo.is_activated == 1:
            book = Book.query.filter_by(id=data['book_id']).first()
            book.status_id = 2

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
        
        livro = Book.query.filter_by(id=emprestimo.book_id).first()
        livro.status_id = 1

        db.session.delete(emprestimo)
        db.session.commit()

        return {'message': 'Empréstimo excluído com sucesso'}
    
    @app.route('/api/emprestimos/devolucao/<int:id>', methods=['PUT'])
    def devolucao(id):
        emprestimo = Loan.query.filter_by(id=id).first()

        if emprestimo is None:
            return {'error': 'Empréstimo não encontrado'}, 404

        emprestimo.is_activated = 0

        book = Book.query.filter_by(id=emprestimo.book_id).first()
        book.status_id = 1

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

    @app.route('/api/emprestimos/renovacao/<int:id>', methods=['PUT'])
    def renovacao(id):
        emprestimo = Loan.query.filter_by(id=id).first()

        if emprestimo is None:
            return {'error': 'Empréstimo não encontrado'}, 404

        emprestimo.return_date = emprestimo.return_date + timedelta(days=15)

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
    
    # livros
    @app.route('/api/livros', methods=['GET'])
    def getLivros():
        livros = Book.query.all()

        return [
            {
                'id': livro.id,
                'title': livro.title,
                'autor': livro.autor,
                'editor': livro.editor if livro.editor else '-',
                'publish_year': livro.publish_year,
                'isbn': livro.isbn,
                'category': livro.category if livro.category else '-',
                'localization': livro.localization if livro.localization else '-',
                'is_activated': livro.is_activated,
                'status_id': livro.status_id,
                'status_name': livro.status.name if livro.status else '-',
            } for livro in livros
        ]
    
    @app.route('/api/livros/<int:id>', methods=['GET'])
    def getLivroById(id):
        livro = Book.query.filter_by(id=id).first()

        if livro is None:
            return {'error': 'Livro não encontrado'}, 404

        return {
            'id': livro.id,
            'title': livro.title,
            'autor': livro.autor,
            'editor': livro.editor if livro.editor else '-',
            'publish_year': livro.publish_year,
            'isbn': livro.isbn,
            'category': livro.category if livro.category else '-',
            'localization': livro.localization if livro.localization else '-',
            'is_activated': livro.is_activated,
            'status_id': livro.status_id,
            'status_name': livro.status.name if livro.status else '-',
        }
    
    @app.route('/api/livros/isbn/<string:isbn>', methods=['GET'])
    def getLivroByIsbn(isbn):
        livro = Book.query.filter_by(isbn=isbn).first()

        if livro is None:
            result = requests.get('https://openlibrary.org/search.json?isbn=' + isbn).json()

            if len(result['docs']) == 0:
                return {'error': 'Livro não encontrado'}
            
            livro = Book(
                title=result['docs'][0]['title'],
                autor=result['docs'][0]['author_name'][0],
                publish_year=result['docs'][0]['first_publish_year'],
                isbn=isbn
            )

            return {
                'id': livro.id,
                'title': livro.title,               
                'autor': livro.autor if livro.autor != '[author not identified]' else None,
                'editor': livro.editor,
                'publish_year': livro.publish_year,
                'isbn': livro.isbn,
                'category': livro.category,
                'localization': livro.localization,
                'is_activated': livro.is_activated,
            }

        return {
            'id': livro.id,
            'title': livro.title,
            'autor': livro.autor,
            'editor': livro.editor,
            'publish_year': livro.publish_year,
            'isbn': livro.isbn,
            'category': livro.category,
            'localization': livro.localization,
            'is_activated': livro.is_activated,
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
            is_activated=data['is_activated'],
            status_id=1
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
            'is_activated': livro.is_activated,
            'status_id': livro.status_id,
            'status_name': livro.status.name if livro.status is not None else None
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
        livro.status_id = data['status_id']

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
            'is_activated': livro.is_activated,
            'status_id': livro.status_id,
            'status_name': livro.status.name
        }
    
    @app.route('/api/livros/delete/<int:id>', methods=['DELETE'])
    def deleteLivro(id):
        livro = Book.query.filter_by(id=id).first()

        if livro is None:
            return {'error': 'Livro não encontrado'}, 404

        db.session.delete(livro)
        db.session.commit()

        return {'message': 'Livro excluído com sucesso'}
    
    @app.route('/api/livros/status', methods=['GET'])
    def getLivrosStatus():
        status = BookStatus.query.all()

        return [
            {
                'id': s.id,
                'name': s.name
            } for s in status
        ]

    return app