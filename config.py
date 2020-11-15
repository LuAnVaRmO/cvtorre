#!/usr/bin/python3


class Config(object):
    SECRET_KEY = 'mysecretkey'


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.0'
    PORT = '5000'
    threaded = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False