from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


# Regexp source: Regular Expressions Cookbook, isbn 9781449319434
class PatientProfileForm(FlaskForm):
    """The form used for displaying and editing patient information"""
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    minitial = StringField("Middle Initial", validators=[Optional()])
    dob = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired()])
    weight = IntegerField("Weight (pounds)", validators=[Optional(), NumberRange(min=0)])
    allergies = StringField("Medication Allergies", validators=[Regexp(
        regex="^[a-zA-Z, ]*$",
        message="Allergies can only contain letters. If more than one, separate by a comma."), Optional()])
    edit = SubmitField("Edit Profile")
    update = SubmitField("Update Profile")
    cancel = SubmitField("Cancel")


class MedicationMainForm(FlaskForm):
    """The form used for main medication page"""
    add_btn = SubmitField("Add Medication")


class MedicationAddForm(FlaskForm):
    """The form used for adding new medications"""
    med_directions = StringField("Directions", validators=[DataRequired()])
    start_date = DateField("Date Started", validators=[Optional()])
    comment = TextAreaField("Comments", validators=[Optional()])
    add_btn = SubmitField("Add")
    cancel_btn = SubmitField("Cancel")


class MedicationEditForm(FlaskForm):
    """The form used for adding new medications"""
    med_directions = StringField("Directions", validators=[DataRequired()])
    start_date = DateField("Date Started", validators=[Optional()])
    comment = TextAreaField("Comments", validators=[Optional()])
    update_btn = SubmitField("Update")
    cancel_btn = SubmitField("Cancel")


class MedicationDeleteForm(FlaskForm):
    """The form used for deleting a medication entry"""
    confirm_btn = SubmitField("Confirm")
    cancel_btn = SubmitField("Cancel")

class MedicationHistoricalAddForm(FlaskForm):
    """The form used for adding new medications"""
    med_directions = StringField("Directions", validators=[DataRequired()])
    end_date = DateField("Date End", validators=[Optional()])
    comment = TextAreaField("Comments", validators=[Optional()])
    add_btn = SubmitField("Add")
    cancel_btn = SubmitField("Cancel")

class MedicationHistoricalEditForm(FlaskForm):
    """The form used for adding new medications"""
    med_directions = StringField("Directions", validators=[DataRequired()])
    end_date = DateField("Date End", validators=[Optional()])
    comment = TextAreaField("Comments", validators=[Optional()])
    update_btn = SubmitField("Update")
    cancel_btn = SubmitField("Cancel")