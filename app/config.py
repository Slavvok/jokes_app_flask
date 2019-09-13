import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATABASE = 'db.sqlite'
    DEBUG = True
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig:
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
