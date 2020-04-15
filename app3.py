# this app is testing the login and registration forms
# (15 april) add FlaskTest>04_Session>app.py: UserMixin class to manage session
# (15 april) add database (sqlalchemy)
import csv
from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, RegisterForm, BookSuggestionForm


# copy from app.py:
import bcrypt
from flask import Flask, session, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import csv
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length, Regexp, ValidationError


app = Flask(__name__)
app.secret_key = 'allo'

# copy from app.py:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username, password=None):
        self.id = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    with open('data/(noah)users.csv') as f:
        for user in csv.reader(f):
            if user[0] == username:
                return User(*user)
    return None



# dummy home link (delete)
@app.route("/")
def home():
    return "<h1>Dummy home page</h1>"


# this register/login appears when clicking on connection button on main menu
@app.route("/Connection", methods=["GET", "POST"])
def connection():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        # here, need to check if registration matches an already existing email/write a function
        # if all is well, send a confirmation email
        return redirect("/registration_redirect", register_form=register_form)
    elif login_form.validate_on_submit():
        return redirect('/')
    # to this return, add empty field that needs to be fill to get redirect page
    return render_template("Register|Login_form.html", form=register_form, form2=login_form)


@app.route("/registration_redirect")
def registration_redirect(register_form):
    return render_template("registration_redirect.html", form=register_form)
# this login page only appears after clicking on email confirmation message


@app.route("/Login")
def email_confirmed():
    return render_template("Login_form.html")


if __name__ == '__main__':
    app.run()
