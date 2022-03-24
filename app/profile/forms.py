from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import date

# Regexp source: Regular Expressions Cookbook, isbn 9781449319434
class PatientProfileForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    minitial = StringField("Middle Initial", validators=[Optional()])
    dob = StringField("Date of Birth", validators=[DataRequired(),
                                                   Regexp("^(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/[0-9]{4}$",
                                                          message="Date of birth must be in the format of MM/DD/YYYY")])
    weight = IntegerField("Weight (pounds)", validators=[Optional(), NumberRange(min=0)])
    edit = SubmitField("Edit Profile")
    update = SubmitField("Update Profile")
    cancel = SubmitField("Cancel")