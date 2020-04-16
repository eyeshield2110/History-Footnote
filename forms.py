from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length, Regexp, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must start with a letter and must have only letters, numbers, dots or underscores')])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(8, 16)])
    password2 = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Login')

class BookSuggestionForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'invalid title')])
    author = StringField("Author", validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'invalid author')])
    submit = SubmitField("Add to Suggestion List")

class UpdateAvatar(FlaskForm):
    icon = FileField('Choose an image for your account icon',
                     validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Upload')