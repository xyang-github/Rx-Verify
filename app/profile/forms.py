from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from datetime import date


class PatientProfileForm(FlaskForm):
    fname = StringField("First Name", render_kw={'readonly': True})
    lname = StringField("Last Name", render_kw={'readonly': True})
    minitial = StringField("Middle Initial", render_kw={'readonly': True})
    dob = StringField("Date of Birth", render_kw={'readonly': True})
    weight = IntegerField("Weight (pounds)", render_kw={'readonly': True})
    edit = SubmitField("Edit Profile")
