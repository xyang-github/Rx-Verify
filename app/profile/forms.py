from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import date


class PatientProfileForm(FlaskForm):
    fname = StringField("First Name", render_kw={'readonly': True}, validators=[DataRequired()])
    lname = StringField("Last Name", render_kw={'readonly': True}, validators=[DataRequired()])
    minitial = StringField("Middle Initial", render_kw={'readonly': True}, validators=[Optional()])
    dob = StringField("Date of Birth", render_kw={'readonly': True}, validators=[DataRequired()])
    weight = IntegerField("Weight (pounds)", render_kw={'readonly': True}, validators=[Optional(), NumberRange(min=0)])
    edit = SubmitField("Edit Profile")
