from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr
import uuid

class User(UserMixin):

    def __init__(self, user_name, password, email):
        super(User, self).__init__()

        self.user_name = user_name
        self.password  = self.hash_password(password)
        self.email = email

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self, user_table):
        ''' Persist user to 'user_table' '''
        user_table.put_item(
            Item={
                'id': str(uuid.uuid1()),
                'user_name' : self.user_name,
                'password'  : self.password,
                'email'     : self.email
            }
        )

    @classmethod
    def get(self, id):
        pass

    @classmethod
    def get_user(cls, user_table, user_name):
        ''' Retrun None if user with 'user_name' not found in 'user_table' '''
        user = user_table.query(
            KeyConditionExpression=Key('user_name').eq(user_name)
        )

        if not user['Items']:
            return None
        data = user['Items'].pop()

        return User(data['user_name'], data['password'], data['email'])

    def get_id(self):
        print("Here") # TODO

