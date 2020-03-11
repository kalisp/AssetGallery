from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from config import Config
from form import login_form
from form import upload_form
from model import user, asset

from flask_s3 import FlaskS3
import flask_s3

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

dynamodb = boto3.resource('dynamodb', region_name=app.config['AWS_REGION'], endpoint_url=app.config['DYNAMODB_ENDPOINT'])
table = dynamodb.Table("Assets")
user_table = dynamodb.Table("Users")

s3 = FlaskS3(app)

s3_upload = boto3.resource('s3',
                    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

# flask_s3.create_all(app)
# quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets')
@login_required
def assets():
    data = table.scan()

    return render_template('assets.html', assets = data['Items'])

@app.route('/assets/tag/<string:tag>')
def tag(tag):
    ''' Print list of assets with same 'tag' '''
    data = table.scan(
        FilterExpression=Attr('tags').contains(tag)
    )
    return render_template('assets.html', assets=data['Items'])

@app.route('/assets/detail/<string:id>')
def detail(id):
    ''' Prints detail of selected asset by its uuid '''
    data = table.query(
            KeyConditionExpression=Key('id').eq(id)
    )
    data = data['Items'][0] if (len(data) > 0) else None
    return render_template('asset_detail.html', asset=data)

@app.route('/assets/upload', methods=['GET', 'POST'])
def upload():
    ''' Upload endpoint, shows form for new asset, handles POST form, endpoint for third party apps'''
    form = upload_form.UploadForm()
    if form.validate_on_submit():  # called only on POST
        screenshot_filename = upload_file(form, 'screenshot')
        asset_filename = upload_file(form, 'asset')

        directory = get_directory() # get real url directory, for S3 with https
        new_asset = asset.Asset(name = form.name.data,
                                author = form.author_name.data,
                                area = form.area.data,
                                tags = form.tags.data,
                                screenshot_path = directory + '/screenshots/' + screenshot_filename,
                                asset_path = directory + '/assets/' + asset_filename
                                )

        table.put_item(
            Item={ key : value for key,value in vars(new_asset).items() if value} # DynamoDB doesnt accept ''
        )
        flash("Asset created!")
        return redirect(url_for('assets'))
    else:
        print("invalid {}".format(form.errors))

    return render_template('upload.html', form=upload_form.UploadForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login form handling '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = login_form.LoginForm()
    if form.validate_on_submit(): # called only on POST
        logged_user = user.User.get_user(user_table, form.user_name.data)
        if logged_user is None or not logged_user.check_password(logged_user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(logged_user)

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

@login_manager.user_loader
def load_user(id):
    ul = user.User.get_user_by_id(user_table, id)
    return user.User.get_user_by_id(user_table, id)

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))

def get_directory():
    ''' Return directory where screenshots and assets are created
        Currently set to S3 location, but could be changed in the future
    '''
    return "https://{}.s3.amazonaws.com".format(app.config['FLASKS3_BUCKET_NAME']) # s3 repository addres

def upload_file(form, typ):
    ''' Uploads file from 'form' to S3
        Called for screenshots and assets. Stored in different folders.
        Currently their persmission is set to 'public-read', that should be modified for prod.
    '''
    if typ == 'screenshot':
        file = form.screenshot_file.data
        filename = secure_filename(form.screenshot_file.data.filename)
    elif typ == 'asset':
        file = form.asset_file.data
        filename = secure_filename(form.asset_file.data.filename)

    obj = s3_upload.Object(app.config['FLASKS3_BUCKET_NAME'], '{}s/{}'.format(typ, filename))
    obj.put(Body=file)
    obj.Acl().put(ACL='public-read')  # TODO dev only - update security for production - probably with pre-signed urls
    return filename

if __name__ == '__main__':

    app.run(debug=True)