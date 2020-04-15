import csv
from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, RegisterForm, BookSuggestionForm


app = Flask(__name__)
# setting the app's secret key like this is not secure, but for now it's good enough to make it work
app.secret_key = 'allo'


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
