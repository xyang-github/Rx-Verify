from flask_login import login_required

from . import profile
from flask import render_template, request, redirect, url_for, flash, session
from .forms import *
from ..db.database_queries import query_select, query_change
from datetime import datetime


@profile.route('/profile', methods=["GET", "POST"])
@login_required
def profile_main():
    """Display profile page"""

    profile_form = PatientProfileForm()

    # Retrieve patient information using patient_id
    patient_id = session['patient_id']
    query = "SELECT * from patient WHERE patient_id = (?)"
    patient = query_select(query, patient_id)

    # Retrieve allergies from patient_allergy table and convert from list of tuples to a string to display
    allergies = query_select(
        query="SELECT allergy FROM patient_allergy WHERE patient_id = (?)",
        key=patient_id
    )
    allergies_list = []
    for allergy in allergies:
        allergies_list.append(allergy[0])
    allergies_string = ", ".join(allergies_list)

    # Make the form display patient's information
    profile_form.fname.data = patient[0][1]
    profile_form.lname.data = patient[0][2]
    profile_form.minitial.data = patient[0][3]
    profile_form.dob.data = datetime.strptime(patient[0][4], '%m-%d-%Y').date()  # convert string to date object
    profile_form.weight.data = patient[0][5]
    profile_form.allergies.data = allergies_string

    # Redirect if the Edit button is clicked
    if profile_form.edit.data:
        return redirect(url_for("profile.edit"))

    return render_template("profile.html", form=profile_form)


@profile.route('/edit', methods=["GET", "POST"])
def edit():
    """Displays page to edit patient profile"""

    profile_form_edit = PatientProfileForm()

    patient_id = session['patient_id']  # will retrieve from the session once login feature has been completed
    query = "SELECT * from patient WHERE patient_id = (?)"
    patient = query_select(query, patient_id)

    # Retrieve allergies in the form of a string
    allergies_string = allergies_db_to_form(patient_id)

    if profile_form_edit.update.data and profile_form_edit.validate():
        # Collect updated data after user clicks the Update button
        fname = request.form['fname']
        lname = request.form['lname']
        minitial = request.form['minitial']
        allergies = request.form['allergies']

        # Convert date object to string; format: YYYY-MM-DD
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        # Change date format to MM-DD-YYYY
        dob = datetime.strftime(dob, "%m-%d-%Y")
        weight = request.form['weight']

        # Update patient table with new information
        sqlite3_variables = [fname, lname, minitial, dob, weight, patient_id]
        query = """
        UPDATE patient 
            SET fname = (?), lname = (?), mname = (?), dob = (?), weight = (?)
            WHERE patient_id = (?);
        """
        query_change(query, sqlite3_variables)

        # Update patient_allergies table - remove current table entries, and enter new ones
        query_change(
            query="DELETE FROM patient_allergy WHERE patient_id = (?)",
            key=(patient_id,)
        )
        allergies_form_to_db(allergies, patient_id)

        flash("Profile has been updated")
        return redirect(url_for("profile.profile_main"))

    if profile_form_edit.cancel.data:
        return redirect(url_for("profile.profile_main"))

    # set form objects to patient information
    profile_form_edit.fname.data = patient[0][1]
    profile_form_edit.lname.data = patient[0][2]
    profile_form_edit.minitial.data = patient[0][3]
    profile_form_edit.dob.data = datetime.strptime(patient[0][4], '%m-%d-%Y').date()
    profile_form_edit.weight.data = patient[0][5]
    profile_form_edit.allergies.data = allergies_string

    return render_template("profile_edit.html", form=profile_form_edit)


def allergies_form_to_db(allergies, patient_id):
    """Take the allergy form entry and write the data to the patient_allergy table"""
    if allergies != "":
        allergies = allergies.split(",")
        for allergy in allergies:
            allergy = allergy.strip()
            query_change(
                query="INSERT OR IGNORE INTO  patient_allergy (patient_id, allergy) VALUES (?, ?)",
                key=[patient_id, allergy]
            )


def allergies_db_to_form(patient_id):
    """Retrieve allergy information from the database (in the form of a list of tuples), and write individual entry
    to the patient_allergy table"""

    allergies = query_select(
        query="SELECT allergy FROM patient_allergy WHERE patient_id = (?)",
        key=patient_id
    )
    allergies_list = []
    for allergy in allergies:
        allergies_list.append(allergy[0])
    allergies_string = ",".join(allergies_list)
    return allergies_string
