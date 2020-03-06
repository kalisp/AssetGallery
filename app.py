from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask_login import LoginManager, current_user, login_user, logout_user

from config import Config
from form import login_form
from model import user

app = Flask(__name__)
#app.secret_key = b'_5#y2L"F4dfse546Q8z\n\xec]/'
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', endpoint_url="http://localhost:8000")
table = dynamodb.Table("Assets")
user_table = dynamodb.Table("Users")

@login_manager.user_loader
def load_user(id):
    print("ID: {}".format(id))
    #return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets')
def assets():
    data = table.scan()
    print(data)
    return render_template('assets.html', assets = data['Items'] * 5)

@app.route('/assets/tag/<string:tag>')
def tag(tag):
    ''' Print list of assets with same 'tag' '''
    print('Tag: {}'.format(tag))
    data = table.scan(
        FilterExpression=Attr('tags').contains(tag)
    )
    print(data)
    return render_template('assets.html', assets=data['Items'])

@app.route('/assets/detail/<string:id>')
def detail(id):
    ''' Prints detail of selected asset by its uuid '''
    data = table.query(
            KeyConditionExpression=Key('id').eq(id)
    )
    data = data['Items'][0] if (len(data) > 0) else None
    return render_template('asset_detail.html', asset=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login form handling '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = login_form.LoginForm()
    if form.validate_on_submit(): # called only on POST
        logged_user = user.User.get_user(user_table, form.user_name.data)
        print("logged user {}".format(logged_user))
        if logged_user is None or not logged_user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)

        flash("Logged in!")
        return redirect(url_for('index'))

    return render_template('login.html', form=login_form.LoginForm())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = login_form.RegisterForm()
    if form.validate_on_submit(): # called only on POST
        registering_user = user.User(form.user_name.data, form.password.data, form.email.data)
        registering_user.save(user_table)
        login_user(registering_user)
        return redirect(url_for('index'))

    return render_template('register.html', form=login_form.RegisterForm())

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)

if __name__ == '__main__':

    app.run(debug=True)