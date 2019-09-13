from app import db
from app.models import Joke
from utils import simple_message
import requests
from flask import request, Blueprint, make_response, request, jsonify
from flask_login import login_user, current_user, login_required
from utils import logging

app = Blueprint('app', __name__)


@app.errorhandler(404)
def joke_404(pk):
    message = f"There is no such joke with id {pk}"
    return simple_message(message, 404)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return make_response(jsonify({"user": current_user.name, "id": current_user.id}))
    else:
        return make_response("Please, log in", 401)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()


@app.route("/generate-joke", methods=['GET', 'POST'])
@login_required
@logging
def create_joke():
    if request.method == 'POST':
        r = requests.get('https://geek-jokes.sameerkumar.website/api').text
        dublicate = False
        joke = db.session.query(Joke).filter_by(joke=r, user_id=current_user.id).first()
        if joke:
            dublicate = True
            return make_response(jsonify({"joke": r, "dublicate": dublicate}), 403)
        joke = Joke(joke=r, user_id=current_user.id)
        db.session.add(joke)
        db.session.commit()
        resp = dict(joke.to_json())
        resp.update({"dublicate": dublicate})
        return make_response(jsonify(resp), 201)


@app.route("/get-jokes-list", methods=['GET'])
@login_required
@logging
def get_jokes_list():
    if request.method == 'GET':
        jokes_list = Joke.query.filter_by(user_id=current_user.id).all()
        return make_response(jsonify(Joke.to_json_list(jokes_list)))


@app.route("/get-joke/<int:pk>", methods=['GET'])
@login_required
@logging
def get_joke(pk):
    if request.method == 'GET':
        joke = Joke.query.filter_by(id=pk, user_id=current_user.id).first()
        if joke:
            return make_response(jsonify(joke.to_json()))
        else:
            return joke_404(pk)


@app.route("/update-joke/<int:pk>", methods=['GET', 'PUT'])
@login_required
@logging
def update_joke(pk):
    if request.method == 'PUT':
        new_joke = request.form['joke']
        item = Joke.query.filter_by(id=pk, user_id=current_user.id).first()
        if item:
            old_joke = item.joke
            if new_joke == old_joke:
                return simple_message("Jokes are identical, cannot update", 403)
            item.joke = new_joke
            db.session.commit()
            return make_response(jsonify({"old_joke": old_joke, "new_joke": new_joke}), 201)
        else:
            return joke_404(pk)


@app.route("/remove-joke/<int:pk>", methods=['GET', 'POST'])
@login_required
@logging
def remove_joke(pk):
    if request.method == 'POST':
        item = Joke.query.filter_by(id=pk, user_id=current_user.id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return simple_message(item.to_json(), 200)
        else:
            return joke_404(pk)