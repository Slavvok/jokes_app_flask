from app import db
from app.models import User
from app import login_manager
from utils import simple_message

from flask import request, Blueprint, url_for, redirect, jsonify
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity

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


@auth.route('/jwt', methods=['POST'])
def login_jwt():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.name == username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token,
                       refresh_token=refresh_token), 200


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user),
    }
    return jsonify(ret), 200


def identity(payload):
    user_id = payload['identity']
    return db.session.query(User).filter(User.id == user_id).first()
