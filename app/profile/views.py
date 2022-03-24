from . import profile
from flask import render_template, request, redirect, url_for, flash
from .forms import *
from ..db.database_queries import query_select


@profile.route('/profile', methods=["GET", "POST"])
def profile_main():
    """Display profile page"""

    profile_form = PatientProfileForm()

    # retrieve patient information using patient_id
    patient_id = 1  # will retrieve from the session once login feature has been completed
    query = "SELECT * from patient WHERE patient_id = (?)"
    patient = query_select(query, patient_id)

    # set form objects to patient information
    profile_form.fname.data = patient[0][1]
    profile_form.lname.data = patient[0][2]
    profile_form.minitial.data = patient[0][3]
    profile_form.dob.data = patient[0][4]
    profile_form.weight.data = patient[0][5]

    # Redirect if the Edit button is clicked
    if profile_form.edit.data:
        return redirect(url_for("profile.edit"))

    return render_template("profile.html", form=profile_form)


@profile.route('/edit', methods=["GET", "POST"])
def edit():
    """Displays page to edit patient profile"""

    profile_form_edit = PatientProfileForm()

    patient_id = 1  # will retrieve from the session once login feature has been completed
    query = "SELECT * from patient WHERE patient_id = (?)"
    patient = query_select(query, patient_id)

    # set form objects to patient information
    profile_form_edit.fname.data = patient[0][1]
    profile_form_edit.lname.data = patient[0][2]
    profile_form_edit.minitial.data = patient[0][3]
    profile_form_edit.dob.data = patient[0][4]
    profile_form_edit.weight.data = patient[0][5]

    if profile_form_edit.validate_on_submit():
        return redirect(url_for("profile.profile_main"))

    return render_template("profile_edit.html", form=profile_form_edit)