from flask import render_template
from . import main


@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@main.route("/guide", methods=["GET", "POST"])
def guide():
    return render_template("guide.html")
