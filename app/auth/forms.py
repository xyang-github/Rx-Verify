from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional, NumberRange
import email_validator


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 50)])
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    minitial = StringField("Middle Initial", validators=[Optional()])
    dob = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired()])
    weight = IntegerField("Weight (pounds)", validators=[Optional(), NumberRange(min=0)])
    allergies = StringField("Medication Allergies (if more than one, separate by space)", validators=[Regexp(
        regex="^[A-Za-z ]+$",
        message="Allergies can only contain letters and spaces")])

    regex = "^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z].*[a-z]).{8,}$"
    message = "Password must have at least 8 characters and include: 1 uppercase letter, 1 lowercase letter, 1 digit, " \
              "1 special character"
    password = PasswordField("Password", validators=[DataRequired(), Regexp(regex, 0, message),
                                                     EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Submit")