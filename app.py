# this app is from A2
# OLD VERSION, DO NOT USE (SEE app4.py)
# (15 apr) 11:15pm This app is the updated version (copy from app4)
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

from readRef import readText2
from create_db2 import Book, Notes, readBookCover, readTitleAuthor_path, \
    readTitleAuthor, readSummary

from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegisterForm, BookSuggestionForm, UpdateAvatar

import bcrypt
from flask import Flask, session, redirect, render_template, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.secret_key = 'hello'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_USERNAME='noe.dinh@gmail.com',
    MAIL_PASSWORD='ilovemuse',
    MAIL_PORT=587,
    # MAIL_US_SSL=True,
    MAIL_USE_TLS=True
)

# setting mail service
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
salt1 = 'email-confirm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'

# copy from app.py:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
# set up database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    icon = db.Column(db.String)


class Book_suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)

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


# global variables from the reading methods
listBookCovers = readBookCover()
pathByTitleAuthor = readTitleAuthor_path()
listTitleAuthor = readTitleAuthor()
listSummaries = readSummary()


@app.route('/')
def home():
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    list_routes = [url_for("active_tab1", x=pathByTitleAuthor[i]) for i in range(len(listBookCovers))]
    display_by_cover = {listBookCovers[i]: list_routes[i] for i in range(len(listBookCovers))}
    return render_template("homepage_unfiltered_menu.html", title="History Footnote: Home",
                           bookList=display_by_cover, username=session.get('username'),
                           icon=icon_path)


# @app.route('/<tag1>/<tag2>')
# def filter(tag1, tag2):
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'
#     filter_paths, indexes = filter_menu_by2(tag1, tag2)
#     list_routes = [url_for("active_tab1", x=filter_paths[i]) for i in range(len(filter_paths))]
#     display_by_cover = {listBookCovers[indexes[i] - 1]: list_routes[i - 1] for i in range(len(indexes))}
#     return render_template("homepage_unfiltered_menu.html", title="History Footnote: Home",
#                            bookList=display_by_cover)


@app.route('/<x>/active_tab1/')
def active_tab1(x):
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    indexBook = pathByTitleAuthor.index(x)
    listTexts = ["", "", "", readText2(("data/Dracula_by_Bram_Stoker.html"))]
    text = readText2("data/" + x + ".html")
    return render_template("page_base_activeTab1.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           integralText=text, tab2="/" + x + "/active_tab2",
                           tab3="/" + x + "/active_tab3", username=session.get('username'),
                           icon=icon_path)


@app.route('/<x>/active_tab2')
def active_tab2(x):
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    indexBook = pathByTitleAuthor.index(x)
    return render_template("page_activeTab2.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           tab3="/" + x + "/active_tab3", tab1="/" + x + "/active_tab1",
                           username=session.get('username'),
                           icon=icon_path)


@app.route('/<x>/active_tab3')
def active_tab3(x):
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    indexBook = pathByTitleAuthor.index(x)
    return render_template("page_activeTab3.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           tab1="/" + x + "/active_tab1", tab2="/" + x + "/active_tab2",
                           username=session.get('username'),
                           icon=icon_path)


@app.route('/archive')
def archive():
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""

    ls_book_sg = Book_suggestion.query.all()
    users = User.query.all()
    return render_template("archive.html", title="History Footnote: Archive", users=users,
                           username=session.get('username'), books=ls_book_sg,
                           icon=icon_path)


@app.route('/about')
def about():
    return render_template("SOEN287_A1_40128079_NOAH-JAMES_DINH.html")


# login methods
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
            return redirect('/login')
    return render_template('login.html', form=login_form)


# # confirmation page: to write
# @app.route('/confirm')
# @login_required # ??
# def login_confirm():
#     return render_template("confirm.html")


# this register/login appears when clicking on connection button on main menu
@app.route("/signup", methods=["GET", "POST"])
def signup():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = find_user(register_form.username.data)
        if not user:
            salt2 = bcrypt.gensalt()
            encrypt_pw = bcrypt.hashpw(register_form.password.data.encode(), salt2)
            new_user = User(username=register_form.username.data, email=register_form.email.data,
                            password=encrypt_pw.decode())
            db.session.add(new_user)
            db.session.commit()

            email = register_form.email.data
            token = serializer.dumps(email, salt=salt1)
            msg = Message('Welcome email from History Footnote', sender="noe.dinh@gmail.com", recipients=[email])
            link = url_for('confirm', token=token, _external=True)
            msg.html = '''
                        <!DOCTYPE html>
                        <html>
                        <body>
                            <h1>Welcome to the website!</h1>
                            <h2>Please click in the following link to login your account:</h2>
                            <a href={}>Login</a>
                            <p>(note that his link will expire within one hour)</p>
                        </body>
                        </html>
                            '''.format(link)
            mail.send(msg)
            return 'Confirmation email sent. Click on the link sent in email to confirm registration within 1h.'
        else:
            flash('Username already taken. Chose another one.')
    return render_template("signup.html", form=register_form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form1 = UpdateAvatar()
    if form1.validate_on_submit():
        f = form1.icon.data  # saves image in 'f'
        filename = secure_filename(f.filename)  # save image name in 'filename'
        f.save(os.path.join('static', filename))
        user = findUser(session.get('username'))
        user.icon = filename
        db.session.commit()
        flash('Profile image updated for {}'.format(session.get('username')))
    username = session.get('username')
    icon_path = ""
    user = findUser(username)
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    return render_template('account.html', form=form1, username=username, email=findUser(username).email
                           , icon=icon_path )


@app.route('/book_suggest', methods=['GET', 'POST'])
@login_required
def book_suggest():
    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    form = BookSuggestionForm()
    if form.validate_on_submit():
        print("validate")
        new_book = Book_suggestion(title=form.title.data, author=form.author.data)
        db.session.add(new_book)
        db.session.commit()
        print("add to db")
        flash('Book suggestion added to list!')
        return redirect('/book_suggest')
    elif form.title.data is None or form.author.data is None:
        flash('You need to add a title/author')
    return render_template('Book_suggestion_form.html', form=form,
                           username=session.get('username'), icon=icon_path)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    # following line does not work, unless i clear session...
    logout_user()
    return redirect('/')


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


# test some Book db handling
@app.route('/check/<title>')
def displayBook(title):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'
    book = Book.query.filter_by(title=title).first()
    print(book.title + " by " + book.author)
    return book.title + " by " + book.author


@app.route("/<time>/<setting>")
def filter_menu_by2(time, setting):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'
    filter_paths =[]
    ls_book_id = []
    list_routes = [url_for("active_tab1", x=pathByTitleAuthor[i]) for i in range(len(listBookCovers))]
    # result = db.session.query(Book).filter(Book.period_tag == time).filter(Book.location_tag == setting)
    result = Book.query.filter_by(location_tag=setting, period_tag=time).all()
    for row in result:
        str_path = row.title + " by " + row.author
        path_as_ls = str_path.split(" ")
        new_path = ""
        for e in path_as_ls:
            new_path += e + "_"
        new_path = new_path[:-1]
        filter_paths.append(new_path)

        book_id = row.id
        ls_book_id.append(book_id)
    display_covers = {listBookCovers[i-1]: list_routes[i-1] for i in ls_book_id}

    icon_path = ""
    user = findUser(session.get('username'))
    if user is not None:
        if user.icon is not None:
            icon_path = user.icon
    else:
        icon_path = ""
    return render_template("homepage_unfiltered_menu.html", bookList=display_covers, title="History", icon=icon_path, username=session.get('username') )


# attempt to set up an email sending route
# @app.route('/<email>', methods=['GET', 'POST'])
def index1(email):
    token = serializer.dumps(email, salt=salt)
    msg = Message('Welcome email from History Footnote', sender="noe.dinh@gmail.com", recipients=[email])
    link = url_for('confirm', token=token, _external=True)
    msg.html = '''
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Welcome to the website!</h1>
                <h2>Please click in the following link to login your account:</h2>
                <a href={}>Login</a>
                <p>(note that his link will expire within one hour)</p>
            </body>
            </html>
                '''.format(link)
    mail.send(msg)
    return 'Confirmation email sent. Click on the link sent in email to confirm registration within 1h.'


# in the following route, user will be add to database and is directed to login page -> home page
# alternatively: use email service to help reset forgotten password
@app.route('/confirm_email/<token>')
def confirm(token):
    try:
        email = serializer.loads(token, salt=salt1, max_age=3600)
    except SignatureExpired:
        return 'The link is expired.'
    flash("New user added to website database!")
    return redirect('/login')





if __name__ == '__main__':
    app.run()
