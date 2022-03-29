from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional, NumberRange
import email_validator


class RegistrationForm(FlaskForm):
    """Define registration form"""
    email = StringField("Email", validators=[DataRequired(message="Email cannot be blank"), Email(), Length(1, 50)])
    fname = StringField("First Name", validators=[DataRequired(message="First name cannot be blank")])
    lname = StringField("Last Name", validators=[DataRequired(message="Last name cannot be blank")])
    minitial = StringField("Middle Initial", validators=[Optional()])
    dob = DateField("Date of Birth", format="%Y-%m-%d",
                    validators=[DataRequired(message="Date of birth cannot be blank")])
    weight = IntegerField("Weight (pounds)", validators=[Optional(), NumberRange(min=0)])
    allergies = StringField("Medication Allergies (if more than one, separate by comma)", validators=[Regexp(
        regex="^[A-Za-z, ]+$",
        message="Allergies can only contain letters, commas, and spaces"), Optional()])

    regex = "^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z].*[a-z]).{8,}$"
    message = "Password must have at least 8 characters and include: 1 uppercase letter, 1 lowercase letter, 1 digit, "\
              "1 special character"
    password = PasswordField("Password", validators=[DataRequired(message="Password cannot be blank"),
                                                     Regexp(regex, 0, message),
                                                     EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """Define login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')