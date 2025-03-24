from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    role = db.Column(db.Text, nullable=False, default='common')
    is_activated = db.Column(db.Boolean, nullable=False, default=True)
    phone = db.Column(db.Text)
    cpf = db.Column(db.Text)
    loans = db.relationship('Loan', backref='user', lazy=True)

class BookStatus(db.Model):
    __tablename__ = 'book_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    autor = db.Column(db.Text, nullable=False)
    editor = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    isbn = db.Column(db.Text)
    category = db.Column(db.Text)
    localization = db.Column(db.Text)
    is_activated = db.Column(db.Boolean, nullable=False, default=True)
    status_id = db.Column(db.Integer, db.ForeignKey('book_status.id'))
    loans = db.relationship('Loan', backref='book', lazy=True)
    status = db.relationship('BookStatus', backref='books', lazy=True)

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)