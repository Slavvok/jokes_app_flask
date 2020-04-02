import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATABASE = 'db.sqlite'
    DEBUG = True
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = datetime.timedelta(minutes=30)


class TestConfig:
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'test.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
