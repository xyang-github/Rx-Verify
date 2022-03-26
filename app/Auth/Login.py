from flask import render_template,redirect, request, url_for, flash, current_app
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous import TimedSerializer as Serializer
from . import main

mail = Mail(main)
login_manager = LoginManager()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

def generate_confirmation_token(self,expiration = 3600):
    s = Serializer(current_app.config['SECRET KEY'],expiration)
    return  s.dumps({'confirm':self.id}).decode('utf-8')

def confirm (self,token):
    s = Serializer(current_app.config['SECRET KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except:
        return False
    if data.get('confirm') != self.id:
        return False
    self.confirmed = True
    db.session.add(self)
    return True

@main.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
    return render_template("index.html")
