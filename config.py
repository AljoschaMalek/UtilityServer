import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'instance', 'utility_server.db')
    DEBUG = True