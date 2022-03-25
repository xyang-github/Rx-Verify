from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

# Regexp source: Regular Expressions Cookbook, isbn 9781449319434
class PatientProfileForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    minitial = StringField("Middle Initial", validators=[Optional()])
    dob = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired()])
    weight = IntegerField("Weight (pounds)", validators=[Optional(), NumberRange(min=0)])
    edit = SubmitField("Edit Profile")
    update = SubmitField("Update Profile")
    cancel = SubmitField("Cancel")