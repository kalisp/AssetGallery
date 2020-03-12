from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr
import uuid

class User(UserMixin):

    def __init__(self, user_name, password, email, id = None):
        super(User, self).__init__()

        self.user_name = user_name
        self.password  = password
        self.email = email
        self.id = id

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, stored_password, password): # TODO refactore
        ''' Compare 'stored_password' hash with hash of 'password' '''
        return check_password_hash(stored_password, password)

    def save(self, user_table):
        ''' Persist user to 'user_table' '''
        self.id = str(uuid.uuid1())
        user_table.put_item(
            Item={
                'id': self.id,
                'user_name' : self.user_name,
                'password'  : self.hash_password(self.password),
                'email'     : self.email
            }
        )


    @classmethod
    def get_user(cls, user_table, user_name):
        ''' Retrun None if user with 'user_name' not found in 'user_table' '''

        user = user_table.query(
            KeyConditionExpression=Key('user_name').eq(user_name)
        )

        if not user['Items']:
            return None
        data = user['Items'].pop()

        return User(data['user_name'], data['password'], data['email'], data['id'])

    @classmethod
    def get_user_by_id(cls, user_table, id):
        ''' Retrun None if user with 'id' not found in 'user_table'.
            Used by flask-login to get user data for each page that is protected by login
        '''
        user = user_table.scan(
            FilterExpression=Key('id').eq(id)
        ) # could be potentially expensive, but fine for now TODO

        if not user['Items']:
            return None
        data = user['Items'].pop()

        return User(data['user_name'], data['password'], data['email'], data['id'])

    def to_dict(self):
        ''' Json representation of User - for API access '''
        data = {
            'id'    : self.id,
            'user_name' : self.user_name,
            #'password'  : self.password, # no real reason why to expose password for now
            'email'     : self.email
        }
        return data