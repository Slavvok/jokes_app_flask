from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
from logging.config import dictConfig

db = SQLAlchemy()
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
                'filename': 'logs/logs.log',
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


def create_app(conf=Config):
    app = Flask(__name__)
    app.config.from_object(conf)
    login_manager.init_app(app)
    db.init_app(app)
    return app

from app import models
