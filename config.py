import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATABASE = 'db.sqlite'
    DEBUG = True
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'test.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
