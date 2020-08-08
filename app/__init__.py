from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from logging.config import dictConfig

login_manager = LoginManager()

dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'logs.log',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'visit_log': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            },
        }
    })


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login = LoginManager()


def create_app(conf=Config):
    """Function for testing"""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(conf)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    jwt.init_app(app)
    return app


from app import models
