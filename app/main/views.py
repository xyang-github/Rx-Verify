from flask import render_template
from . import main


@main.route("/", methods=["GET", "POST"])
def index():
    """View function for the main splash page"""
    return render_template("index.html")


@main.route("/guide", methods=["GET", "POST"])
def guide():
    """View function for the user guide page"""
    return render_template("guide.html")
