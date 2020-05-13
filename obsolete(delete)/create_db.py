# this module creates db for the books viewed on website.
# This database cannot be modified by users via FlaskForm on server
# for this test-app, no app.routes are created
# the purpose of this app is to create the db "books_db.sqlite3" that we will then
# connect to the main Flask app...
# !!! FORGOT A COLUMN (book cover), copy this app to create_db2.py

import sqlite3
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'allo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db.sqlite3'

db = SQLAlchemy(app)


# each book has variable numbers of notes; create another database for the notes and store address of notes in
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    summary = db.Column(db.String)
    period_tag = db.Column(db.String)
    location_tag = db.Column(db.String)
    notes = db.relationship('Notes', backref='a_book')



class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_in_html = db.Column(db.String)
    content_of_note = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey('book.title'))


filename = 'book_database.db'

