import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key' # or part only for dev!