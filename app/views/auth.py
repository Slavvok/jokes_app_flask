from app import db
from app.models import User
from app import login_manager
from utils import simple_message

from flask import request, Blueprint, url_for, redirect
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()


@auth.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
        email = data['email']
        if not (db.session.query(User).filter_by(name=username).first()
                and db.session.query(User).filter_by(email=email).first()):
            u = User(username, email)
            u.generate_hash(password)
            db.session.add(u)
            db.session.commit()
        else:
            return simple_message("User with that name/email already exists", 403)
        return simple_message(f"User {u.name} was created", 201)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
        user = db.session.query(User).filter(User.name == username).first()
        if user and user.check_password(password):
            login_user(user)
        return redirect(url_for('app.index'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('app.index'))

