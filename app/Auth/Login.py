from flask import render_template
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField
from . import main

mail = Mail(main)

class NameForm(FlaskForm):
    name = StringField()

@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
    return render_template("index.html")
