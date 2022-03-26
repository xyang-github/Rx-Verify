from flask import render_template,redirect, request, url_for, flash
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from flask_login import LoginManager, login_user, logout_user, login_required
from . import main

mail = Mail(main)
login_manager = LoginManager()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

@main.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
    return render_template("index.html")
