import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = datetime.timedelta(minutes=30)


class TestConfig(Config):
    SECRET_KEY = 'dsasdfdfadfadsfa'
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class ProductionConfig:
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
