from flask import render_template, redirect, url_for, flash
from . import main



@main.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")