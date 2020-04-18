from app import db
from app.models import Joke
from utils import simple_message
import requests
from flask import request, Blueprint, make_response, request, jsonify
from flask_jwt import current_identity
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token
from utils import logging
from app.views.auth import login_jwt, identity

jokes = Blueprint('jokes', __name__)

jwt = JWTManager(app)


@jokes.errorhandler(404)
def joke_404(pk):
    message = f"There is no such joke with id {pk}"
    return simple_message(message, 404)


# @jokes.route('/')
# def index():
#     if current_user.is_authenticated:
#         return make_response(jsonify({"user": current_identity.name, "id": current_identity.id}))
#     else:
#         return make_response("Please, log in", 401)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()

@jokes.route("/generate-joke", methods=['POST'])
@jwt_required
@logging
def generate_joke():
    if request.method == 'POST':
        r = requests.get('https://geek-jokes.sameerkumar.website/api').text
        dublicate = False
        joke = db.session.query(Joke).filter_by(joke=r, user_id=get_jwt_identity()).first()
        if joke:
            dublicate = True
            return make_response(jsonify({"joke": r, "dublicate": dublicate}), 403)
        joke = Joke(joke=r, user_id=get_jwt_identity())
        db.session.add(joke)
        db.session.commit()
        resp = dict(joke.to_json())
        resp.update({"dublicate": dublicate})
        return make_response(jsonify(resp), 201)


@jokes.route("/get-jokes-list", methods=['GET'])
@jwt_required
@logging
def get_jokes_list():
    if request.method == 'GET':
        jokes_list = Joke.query.filter_by(user_id=get_jwt_identity()).all()
        return make_response(jsonify(Joke.to_json_list(jokes_list)))


@jokes.route("/get-joke/<int:pk>", methods=['GET'])
@jwt_required
@logging
def get_joke(pk):
    if request.method == 'GET':
        joke = Joke.query.filter_by(id=pk, user_id=get_jwt_identity()).first()
        if joke:
            return make_response(jsonify(joke.to_json()))
        else:
            return joke_404(pk)


@jokes.route("/update-joke/<int:pk>", methods=['GET', 'PUT'])
@jwt_required
@logging
def update_joke(pk):
    if request.method == 'PUT':
        new_joke = request.json['joke']
        item = Joke.query.filter_by(id=pk, user_id=get_jwt_identity()).first()
        if item:
            old_joke = item.joke
            if new_joke == old_joke:
                return simple_message("Jokes are identical, cannot update", 403)
            item.joke = new_joke
            db.session.commit()
            return make_response(jsonify({"old_joke": old_joke, "new_joke": new_joke}), 201)
        else:
            return joke_404(pk)


@jokes.route("/remove-joke/<int:pk>", methods=['GET', 'POST'])
@jwt_required
@logging
def remove_joke(pk):
    if request.method == 'POST':
        item = Joke.query.filter_by(id=pk, user_id=get_jwt_identity()).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return simple_message(item.to_json(), 200)
        else:
            return joke_404(pk)