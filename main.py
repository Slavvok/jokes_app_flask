from flask import request, jsonify, make_response, Blueprint
import requests
from flask_login import current_user, login_required
from app import create_app, db
from utils import logging
from app.views import auth, jokes
from utils import simple_message
from flask import Blueprint

app = create_app()
with app.app_context():
    db.create_all()
app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(jokes.app)

from app.models import Joke, User

if __name__ == '__main__':
	app.run()

