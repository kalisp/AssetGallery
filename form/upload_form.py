from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author_name = StringField('Author', validators=[DataRequired()])
    area = SelectField('Area', choices = [('animation', 'Animation'), ('model', 'Model')])
    screenshot_file = FileField('Screenshot', validators=[FileRequired()])
    asset_file = FileField('Asset') # , validators=[FileRequired()]
    tags = StringField('Tags')

    submit = SubmitField('Upload')