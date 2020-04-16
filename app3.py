# this app is testing the login and registration forms
# 15 april (8:30pm) Basic signup and login work
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
app.secret_key = '1234'

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
    with open('data/users.csv') as f:
        for user in csv.reader(f):
            if user[0] == username:
                return User(*user)
    return None


# dummy home link (delete)
@app.route("/")
def home():
    return render_template('(noah)home.html', username= session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = find_user(login_form.username.data)
        if user and bcrypt.checkpw(login_form.password.data.encode(), user.password.encode()):
            login_user(user)
            flash('Logged in successfully.')
            session['username'] = user.id
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Wrong password or username')
        return redirect('/')
    return render_template('login.html', form=login_form)


# this register/login appears when clicking on connection button on main menu
@app.route("/signup", methods=["GET", "POST"])
def signup():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = find_user(register_form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            encrypt_pw = bcrypt.hashpw(register_form.password.data.encode(), salt)
            with open('data/users.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([register_form.username.data, encrypt_pw.decode()])
            flash('Successful registration. Check email for confirmation link.')
            return redirect(url_for("login"))
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
    return "<h1>This is a third page. </h1> The user " + session.get('username') + " has access."


@app.route('/public')
def public():
    return "<h1>This is a public page with nothing to show... </h1>"


if __name__ == '__main__':
    app.run()
