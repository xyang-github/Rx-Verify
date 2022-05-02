from flask_wtf import FlaskForm
from wtforms import *


class DrugInteractionForm(FlaskForm):
    """Form fields for the drug interaction page"""
    drug_list = SelectMultipleField("Medication list")
    btn_add = SubmitField("Add")
    btn_remove = SubmitField("Remove")
    btn_submit = SubmitField("Submit")
