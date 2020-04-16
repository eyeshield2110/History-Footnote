# copy of create_db
# this Book table has a cover column (link)
# !!! forgot to add path to integral texts... create it afterward
# use the path by titleAuthor to name the integral texts

import sqlite3
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'allo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'

db = SQLAlchemy(app)


# each book has variable numbers of notes; create another database for the notes and store address of notes in
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    summary = db.Column(db.String)
    cover = db.Column(db.String)
    period_tag = db.Column(db.String)
    location_tag = db.Column(db.String)
    notes = db.relationship('Notes', backref='a_book')


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_in_html = db.Column(db.String)
    content_of_note = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey('book.title'))


filename = 'book_database.db'


# this method generates a book_counter (purpose: looping) to display the book on main menu
def main_menu():
    enum_books = Book.query.all()
    # num_books = enum_books.length
    counter = 1
    for book in enum_books:
        select_book = Book.query.filter_by(id=counter).first()
        print(select_book.title)
        counter += 1


# this method has same function as original "readBookCover()" method from readRef
# return a list with the links to the book cover
def readBookCover():
    enum_books = Book.query.all()
    book_cover = []
    counter = 1
    for book in enum_books:
        select_book = Book.query.filter_by(id=counter).first()
        book_cover.append(select_book.cover)
        counter += 1
    return book_cover


def readTitleAuthor_path():
    enum_books = Book.query.all()
    paths = []
    counter = 1
    for book in enum_books:
        select_book = Book.query.filter_by(id=counter).first()
        str_title_author = select_book.title + " by " + select_book.author
        list_title_author = str_title_author.split(" ")
        new_str = ""
        for e in list_title_author:
            new_str += e + "_"
        new_str = new_str[:-1]
        paths.append(new_str)
        counter += 1
    return paths


def readTitleAuthor():
    enum_books = Book.query.all()
    books = []
    counter = 1
    for book in enum_books:
        select_book = Book.query.filter_by(id=counter).first()
        str_title_author = select_book.title + " by " + select_book.author
        books.append(str_title_author)
        counter += 1
    return books


def readSummary():
    enum_books = Book.query.all()
    summaries = []
    counter = 1
    for book in enum_books:
        select_book = Book.query.filter_by(id=counter).first()
        summaries.append(select_book.summary)
        counter += 1
    return summaries


# return paths for filter menu
def filter_menu_by(tag_type, tag_value):
    filter_paths = []
    if tag_type == "period_tag":
        result = db.session.query(Book).filter(Book.period_tag == tag_value)
        for row in result:
            str_path = row.title + " by " + row.author
            path_as_ls = str_path.split(" ")
            new_path = ""
            for e in path_as_ls:
                new_path += e + "_"
            new_path = new_path[:-1]
            filter_paths.append(new_path)
    elif tag_type == "location_tag":
        result = db.session.query(Book).filter(Book.location_tag == tag_value)
        for row in result:
            str_path = row.title + " by " + row.author
            path_as_ls = str_path.split(" ")
            new_path = ""
            for e in path_as_ls:
                new_path += e + "_"
            new_path = new_path[:-1]
            filter_paths.append(new_path)
    return filter_paths


def filter_menu_by2(time, setting): # time and location (in this order)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'
    filter_paths =[]
    ls_book_id = []
    # result = db.session.query(Book).filter(Book.period_tag == time).filter(Book.location_tag == setting)
    result = Book.query.filter_by(period_tag=time).filter_by(location_tag=setting).all()
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
    return filter_paths, ls_book_id
