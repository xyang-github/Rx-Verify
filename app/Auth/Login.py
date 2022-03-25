from flask import render_template, redirect, url_for
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
    if form.validate_on_submit():
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template("index.html")

#Email support
def send_email():
    msg = Message
    mail.send(msg)
