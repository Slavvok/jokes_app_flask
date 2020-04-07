from flask_login import UserMixin
from app import db
import hashlib
import os
import hmac
from sqlalchemy.inspection import inspect


class Serializer:
    format = []

    def to_json(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys() if c in self.format}

    @staticmethod
    def to_json_list(l):
        return [i.to_json() for i in l]


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, )
    _password_hash = db.Column(db.String(128))
    _salt = db.Column(db.String(128))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def generate_hash(self, password):
        self._salt = os.urandom(16).hex()
        self._password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                  bytes.fromhex(self._salt), 10000).hex()

    def check_password(self, password):
        return hmac.compare_digest(
            self._password_hash,
            hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(self._salt), 10000).hex()
        )

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Joke(db.Model, Serializer):
    __tablename__ = 'jokes'
    id = db.Column(db.Integer, primary_key=True)
    joke = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    format = ['id', 'joke']

    def __repr__(self):
        return f"{self.id} {self.joke}"
