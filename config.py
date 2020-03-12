import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key' # or part only for dev!
    FLASKS3_BUCKET_NAME = ''
    AWS_REGION = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    FLASKS3_DEBUG = True
    DYNAMODB_ENDPOINT = ''