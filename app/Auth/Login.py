from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail
from flask_mail import Message
from . import main

mail = Mail(main)

class NameForm(FlaskForm):
    name = StringField('Test1',validators=[DataRequired()])
    submit = SubmitField('Submit')

@main.route("/", methods=["GET", "POST"])
def index():
    form =NameForm()
    return render_template("index.html")

#Email support
def send_email():
    msg = Message
    mail.send(msg)
