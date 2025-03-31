from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    password = db.Column(db.String(256))
    role = db.Column(db.Text, nullable=False, default='common')
    is_activated = db.Column(db.Boolean, nullable=False, default=True)
    phone = db.Column(db.Text)
    cpf = db.Column(db.Text)