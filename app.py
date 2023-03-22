import json

from flask import Flask, render_template, request
import GoogleAcademyService
import DBHelper
import BaseMapper

app = Flask(__name__)


@app.route("/")
def index_page():
    dataPage = DBHelper.select_all_authors()
    return render_template("index.html", datas=dataPage)


@app.route("/searchName/")
def searchName():
    author_name = request.args.get("name")
    data = GoogleAcademyService.searchByAuthorName(author_name.strip())

    if data is None:
        return render_template("error.html", message="Автор не найден!")

    dataToSave = (data["name"], data["hindex"], data["i10index"], data["imgUrl"], data["resource"])

    duplicateChecker = DBHelper.select_all_authors()
    for i in duplicateChecker:
        if str(i[2]) == data["name"]:
            dataForUpdate = (data["hindex"], data["i10index"], data["imgUrl"], i[0])
            DBHelper.updateAuthor(dataForUpdate)
            return render_template("error.html", message="Автор уже существует в нашей базе данных! ДАННЫЕ "
                                                         "СИНХРОНИЗИРОВАНЫ")
    DBHelper.createAuthor(dataToSave)
    return render_template("result.html", data=data)


@app.route("/filter/")
def filterAuthors():
    filterKey = request.args.get("select")
    if filterKey == "hindex":
        dataH = DBHelper.filterAuthors(filterKey)
        return render_template("index.html", datas=dataH, sess1="selected")
    if filterKey == "i10index":
        dataI = DBHelper.filterAuthors(filterKey)
        return render_template("index.html", datas=dataI, sess2="selected")
    return render_template("index.html", filterErr="Не правильный фильтр")


# API RESOURCE
@app.route('/api/authors/')
def allAuthors():
    authors = BaseMapper.convertToAuthorsJson(DBHelper.select_all_authors())
    return json.dumps(authors)


@app.route('/api/authors/<int:author_id>')
def findAuthorById(author_id=None):
    author = BaseMapper.convertToAuthorsJson(DBHelper.findAuthorById(author_id))
    if author:
        return json.dumps(author)
    return json.dumps({"message": f"Не найден автор с id : {author_id}"})


@app.route('/api/authors/<authorName>')
def findAuthorByNameContains(authorName=None):
    authorsList = BaseMapper.convertToAuthorsJson(DBHelper.findAuthorByNameContains(authorName))
    return json.dumps(authorsList)


@app.route('/api/authors/filter/<filterKey>')
def filterAuthorsBy(filterKey=None):
    authorsList = BaseMapper.convertToAuthorsJson(DBHelper.filterAuthors(filterKey))
    if authorsList:
        return json.dumps(authorsList)
    return json.dumps({"message": f"Неправильный фильтр : {filterKey}"})


if __name__ == '__main__':
    app.run()
