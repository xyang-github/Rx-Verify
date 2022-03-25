from flask import render_template
from flask_mail import Mail
from . import main

mail = Mail(main)

@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
