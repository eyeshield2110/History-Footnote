import urllib3
import urllib.request
with urllib.request.urlopen('http://python.org/') as response:
   html = response.read()
   print(html)

def readBookCover():
    with open("data/book_cover.txt") as f:
        book_covers = [link[:-1] if link[-1] == "\n" else link for link in f.readlines()]
    return book_covers


def readTitleAuthor():
    with open("data/title_author.txt") as f:
        title_author = [link[:-1] if link[-1] == "\n" else link for link in f.readlines()]
    return title_author


def readTitleAuthor_path():
    with open("data/title_author.txt") as f:
        title_author = [link[:-1] if link[-1] == "\n" else link for link in f.readlines()]
        for i in range(len(title_author)):
            link_as_list = title_author[i].split(" ")
            link2 = ""
            for s in link_as_list:
                link2 += s + "_"
            title_author[i] = link2

    return [link[:-1] for link in title_author]


def readSummary():
    with open("data/summaries.txt") as f:
        summaries = [summary[:-1] if summary[-1] == "\n" else summary for summary in f.readlines()]
    return summaries


def readText():
    with open("data/integral_texts.txt") as f:
        texts = [text[:-1] if text[-1] == "\n" else text for text in f.readlines()]
    return texts

def readText2(file):
    if file == "":
        return "text not available :)"
    with open(file) as f:
        texts = [text[:-1] if text[-1] == "\n" else text for text in f.readlines()]
        text_without_empty = []
        for line in texts:
            if line!="":
                text_without_empty.append(line)

    return text_without_empty




