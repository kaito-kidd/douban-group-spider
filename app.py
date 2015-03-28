# coding: utf8

import re

from flask import Flask, request, render_template
from dbmixin import DBMixin

app = Flask(__name__)
app.debug = True

# db & collection
db = DBMixin().db
collection = db.result_topic

@app.route("/", methods=["GET", "POST"])
def index():
    """index
    """
    keyword = request.form.get("keyword", "")
    where = {}
    if keyword:
        regx = re.compile(".*%s.*" % keyword, re.IGNORECASE)
        where["title"] = {"$regex": regx}
    topics = collection.find(where) \
        .sort([("create_time", -1)]).limit(300)
    return render_template(
        "index.html",
        topics=topics,
        keyword=keyword)

if __name__ == "__main__":
    app.run()
