# this app is a copy of app(1); app4 is as of now the most recent version of this project
# (1) Database for books

from readRef import readText, readText2

# from create_db2 module
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from create_db2 import Book, Notes, readBookCover, readTitleAuthor_path, \
    readTitleAuthor, readSummary, filter_menu_by2

app = Flask(__name__)
app.secret_key = 'allo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db2.sqlite3'

db = SQLAlchemy(app)

# global variables from the reading methods
listBookCovers = readBookCover()
pathByTitleAuthor = readTitleAuthor_path()
listTitleAuthor = readTitleAuthor()
listSummaries = readSummary()


@app.route('/')
def home():
    list_routes = [url_for("active_tab1", x=pathByTitleAuthor[i]) for i in range(len(listBookCovers))]
    display_by_cover = {listBookCovers[i]: list_routes[i] for i in range(len(listBookCovers))}
    return render_template("templates/homepage_unfiltered_menu.html", title="History Footnote: Home",
                           bookList=display_by_cover)


@app.route('/<tag1>/<tag2>')
def filter(tag1, tag2):
    filter_paths, indexes = filter_menu_by2(tag1, tag2)
    list_routes = [url_for("active_tab1", x=filter_paths[i]) for i in range(len(filter_paths))]
    display_by_cover = {listBookCovers[indexes[i]-1]: list_routes[i-1] for i in range(len(indexes))}
    return render_template("templates/homepage_unfiltered_menu.html", title="History Footnote: Home",
                           bookList=display_by_cover)


@app.route('/<x>/active_tab1/')
def active_tab1(x):
    indexBook = pathByTitleAuthor.index(x)
    listTexts = ["", "", "", readText2(("data/Dracula_by_Bram_Stoker.html"))]
    return render_template("templates/page_base_activeTab1.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           integralText=listTexts[indexBook], tab2="/"+x+"/active_tab2", tab3="/"+x+"/active_tab3")


@app.route('/<x>/active_tab2')
def active_tab2(x):
    indexBook = pathByTitleAuthor.index(x)
    return render_template("templates/page_activeTab2.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           tab3="/"+x+"/active_tab3", tab1="/"+x+"/active_tab1")


@app.route('/<x>/active_tab3')
def active_tab3(x):
    indexBook = pathByTitleAuthor.index(x)
    return render_template("templates/page_activeTab3.html", bookCover=listBookCovers[indexBook],
                           title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook],
                           tab1="/"+x+"/active_tab1", tab2="/"+x+"/active_tab2")


@app.route('/archive')
def archive():
    return render_template("templates/archive.html", title="History Footnote: Archive")


@app.route('/about')
def about():
    return render_template("templates/SOEN287_A1_40128079_NOAH-JAMES_DINH.html")


if __name__ == '__main__':
    app.run()