# this app is testing the login and registration forms
# 15 april (8:30pm) Basic signup and login work
import csv
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

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
app.secret_key = '1234'

# copy from app.py:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
# set up database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    icon = db.Column(db.String)


# do not add email to userMixin, i think thats what fuck up last time
class User_session(UserMixin):
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
    user_in_db = findUser(username)
    if user_in_db:
        return User_session(user_in_db.username, user_in_db.password)
    return None


# dummy home link (delete)
@app.route("/")
def home():
    return render_template('(noah)home.html', username=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_session = find_user(login_form.username.data)
        if user_session and bcrypt.checkpw(login_form.password.data.encode(), user_session.password.encode()):
            login_user(user_session)
            flash('Logged in successfully.')
            session['username'] = user_session.id
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Wrong password or username')
        return redirect('/')
    return render_template('login.html', form=login_form)


# confirmation page: to write
@app.route('/confirm')
def login_confirm():
    return "user added to db"


# this register/login appears when clicking on connection button on main menu
@app.route("/signup", methods=["GET", "POST"])
def signup():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = find_user(register_form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            encrypt_pw = bcrypt.hashpw(register_form.password.data.encode(), salt)
            new_user = User(username=register_form.username.data, email=register_form.email.data,
                            password=encrypt_pw.decode())
            db.session.add(new_user)
            db.session.commit()
            flash('Check email for link to confirm registration.')
            return redirect("/confirm")
        else:
            flash('Username already taken. Chose another one.')
    return render_template("signup.html", form=register_form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    # following line does not work, unless i clear session...
    logout_user()
    return redirect('/')


@app.route('/private1')
@login_required
def private1():
    return "<h1>This is a private page. </h1> The user " + session.get('username') + " has access."


@app.route('/private2')
@login_required
def private2():
    return "<h1>This is a second private page. </h1> The user " + session.get('username') + " has access."


@app.route('/private3')
@login_required
def private3():
    return """
    <h1>This is a third page. </h1> The user " + session.get('username') + " has access."""


@app.route('/public')
def public():
    return """
    <h1>This is a public page with nothing to show... </h1>"""


# a few methods to add/delete/display users
def displayAllUsers():
    users = User.query.all()
    for user in users:
        print("username: " + user.username + ", email:" + user.email
              + ", encoded_pw:" + user.password)


def displayUser(un):
    user = User.query.filter_by(username=un).first()
    try:
        print(user.username, 'is in database')
        return user.username + 'is in database'
    except AttributeError as e:
        print('There are no users by this username')
        return 'There are no users by this username'


def addUser(username, email, password, icon):
    user = User(username=username, email=email, password=password, icon=icon)
    db.session.add(user)
    db.session.commit()


def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()

def findUser(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user
    else:
        return None

if __name__ == '__main__':
    app.run()
