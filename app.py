# this app is from A2
# need to copy this to app4 and rewrite readRef + reorganize data into database/s
from flask import Flask, url_for, render_template

from readRef import readBookCover, readTitleAuthor_path, readTitleAuthor, readSummary, readText, readText2



app = Flask(__name__)


@app.route('/')
def home():
    listBookCovers = readBookCover()
    pathByTitleAuthor = readTitleAuthor_path()
    list_routes = [url_for("active_tab1", x=pathByTitleAuthor[i]) for i in range(len(listBookCovers))]
    display_by_cover = {listBookCovers[i]: list_routes[i] for i in range(len(listBookCovers))}
    return render_template("homepage_unfiltered_menu.html", title = "History Footnote: Home", bookList=display_by_cover)

@app.route('/<x>/active_tab1/')
def active_tab1(x):
    pathByTitleAuthor = readTitleAuthor_path()
    indexBook = pathByTitleAuthor.index(x)
    listBookCovers = readBookCover()
    listTitleAuthor = readTitleAuthor()
    listSummaries = readSummary()
    #listTexts = readText()
    listTexts = ["", "", "", readText2(("ref/DraculaText.html"))]
    return render_template("page_base_activeTab1.html", bookCover=listBookCovers[indexBook], title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook], integralText=listTexts[indexBook], tab2="/"+x+"/active_tab2", tab3="/"+x+"/active_tab3")

@app.route('/<x>/active_tab2')
def active_tab2(x):
    pathByTitleAuthor = readTitleAuthor_path()
    indexBook = pathByTitleAuthor.index(x)
    listBookCovers = readBookCover()
    listTitleAuthor = readTitleAuthor()
    listSummaries = readSummary()
    return render_template("page_activeTab2.html", bookCover=listBookCovers[indexBook], title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook], tab3="/"+x+"/active_tab3", tab1="/"+x+"/active_tab1")

@app.route('/<x>/active_tab3')
def active_tab3(x):
    pathByTitleAuthor = readTitleAuthor_path()
    indexBook = pathByTitleAuthor.index(x)
    listBookCovers = readBookCover()
    listTitleAuthor = readTitleAuthor()
    listSummaries = readSummary()
    return render_template("page_activeTab3.html", bookCover=listBookCovers[indexBook], title=listTitleAuthor[indexBook], bookSummary=listSummaries[indexBook], tab1="/"+x+"/active_tab1", tab2="/"+x+"/active_tab2")

@app.route('/archive')
def archive():
    return render_template("archive.html", title="History Footnote: Archive")

@app.route('/about')
def about():
    return render_template("SOEN287_A1_40128079_NOAH-JAMES_DINH.html")


if __name__ == '__main__':
    app.run()
