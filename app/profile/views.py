import requests
from flask_login import login_required
from . import profile
from flask import render_template, request, redirect, url_for, flash, session
from .forms import *
from .table import Active_Medications_Table
from .table import Historical_Medications_Table
from ..db.database_queries import query_select, query_change, query_medication_results
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


@profile.route('/medmain', methods=["GET", "POST"])
@login_required
def medmain():
    # Display the medication page

    # Instantiate the medication main form into a variable
    main_medication_form = MedicationMainForm()

    # Get the patient_id from flask session
    patient_id = session['patient_id']

    # Use patient_id to get the patient's list of active medications. Note that Flask-Table requires a list of
    # dictionaries, which is why a new function 'query_medication_results' is used instead of 'query_select'
    list_of_active_medications = query_medication_results(
        query="SELECT active_med_id, active_med.patient_id, med_name, med_dose, med_directions, med_start_date, "
              "comment, rxcui from active_med INNER JOIN  patient ON active_med.patient_id = patient.patient_id WHERE "
              "active_med.patient_id = (?)",
        key=str(patient_id)
    )

    list_of_historical_medications = query_medication_results(
        query="SELECT hist_med_id, hist_med.patient_id, med_name, med_dose, med_directions, med_end_date, "
              "comment, rxcui from hist_med INNER JOIN  patient ON hist_med.patient_id = patient.patient_id WHERE "
              "hist_med.patient_id = (?)",
        key=str(patient_id)
    )

    if len(list_of_active_medications) > 0 or len(list_of_historical_medications) > 0:

        # Store the results in a table using Flask-Table module
        table = Active_Medications_Table(list_of_active_medications)
        historical_table = Historical_Medications_Table(list_of_historical_medications)
        return render_template("med.html", form=main_medication_form, active_meds=list_of_active_medications,
                               historical_meds= list_of_historical_medications, table=table, historical_table = historical_table)
    # Enter code for historical medications here

    return render_template("med.html", form=main_medication_form, active_meds=list_of_active_medications)


@profile.route('/med_add', methods=["GET", "POST"])
@login_required
def active_medication_add():
    """Displays the add medication page"""

    # Instantiate form object
    medication_form = MedicationAddForm()

    # Clicking the cancel button will go back to medmain page
    if medication_form.cancel_btn.data:
        return redirect(url_for("profile.medmain"))

    # Clicking the add button will validate form field entries
    if medication_form.add_btn.data:

        # Store form fields into their own variables
        med_directions = medication_form.med_directions.data
        start_date = medication_form.start_date.data
        comment = medication_form.comment.data

        # Store the med name and dose in their own variables; the syntax is different, because the form fields do not
        # use FlaskForm
        med_name = request.form['rxterms']
        med_dose = request.form['drug_strengths']

        # Will display a warning if medication name field is blank
        if med_name == "":
            flash("Medication name cannot be blank")

        # Will display a warning if medication strength field is blank
        elif med_dose == "":
            flash("Medication strength cannot be blank")

        else:

            # Construct url needed to send a request to RxTerms API
            url_base = "https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms="
            url_final = url_base + med_name + "&ef=STRENGTHS_AND_FORMS,RXCUIS"

            # Send a request to RxTerms API
            response = requests.get(url_final).json()

            # A value of 1 means that one exact match for the name was found
            if response[0] >= 1:

                # Create a list of doses associated with the drug name, stripped of leading white space
                list_of_doses = []
                for dose in response[2]['STRENGTHS_AND_FORMS'][0]:
                    list_of_doses.append(dose.strip())

                # Determine if the dose entered in the form matches a dose in RxTerms; if there is a match, will
                # get the rxcui which will be later used in the API
                try:
                    dose_index = list_of_doses.index(med_dose)
                    rxcui = response[2]['RXCUIS'][0][dose_index]

                    # Add new medication entry to the database
                    query_change(
                        query="INSERT INTO active_med (patient_id, med_name, med_dose, med_directions, med_start_date, "
                              "comment, rxcui) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        key=[session['patient_id'], med_name, med_dose, med_directions, start_date, comment, rxcui]
                    )

                    # Shows a message that medication has been added, and redirects to medmain
                    flash("Medication has been added")
                    return redirect(url_for("profile.medmain"))

                except ValueError:
                    flash("The medication strength entered does not exist.")

            # A value of 0 means there is no match for the medication name
            else:
                flash("The medication name entered does not exist.")

    return render_template("active_med_add.html", form=medication_form)

@profile.route('/historical_med_add', methods=["GET", "POST"])
@login_required
def historical_medication_add():
    """Displays the add medication page"""

    # Instantiate form object
    medication_form = MedicationHistoricalAddForm()

    # Clicking the cancel button will go back to medmain page
    if medication_form.cancel_btn.data:
        return redirect(url_for("profile.medmain"))

    # Clicking the add button will validate form field entries
    if medication_form.add_btn.data:

        # Store form fields into their own variables
        med_directions = medication_form.med_directions.data
        end_date = medication_form.end_date.data
        comment = medication_form.comment.data

        # Store the med name and dose in their own variables; the syntax is different, because the form fields do not
        # use FlaskForm
        med_name = request.form['rxterms']
        med_dose = request.form['drug_strengths']

        # Will display a warning if medication name field is blank
        if med_name == "":
            flash("Medication name cannot be blank")

        # Will display a warning if medication strength field is blank
        elif med_dose == "":
            flash("Medication strength cannot be blank")

        else:

            # Construct url needed to send a request to RxTerms API
            url_base = "https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms="
            url_final = url_base + med_name + "&ef=STRENGTHS_AND_FORMS,RXCUIS"

            # Send a request to RxTerms API
            response = requests.get(url_final).json()

            # A value of 1 means that one exact match for the name was found
            if response[0] >= 1:

                # Create a list of doses associated with the drug name, stripped of leading white space
                list_of_doses = []
                for dose in response[2]['STRENGTHS_AND_FORMS'][0]:
                    list_of_doses.append(dose.strip())

                # Determine if the dose entered in the form matches a dose in RxTerms; if there is a match, will
                # get the rxcui which will be later used in the API
                try:
                    dose_index = list_of_doses.index(med_dose)
                    rxcui = response[2]['RXCUIS'][0][dose_index]

                    # Add new medication entry to the database
                    query_change(
                        query="INSERT INTO hist_med (patient_id, med_name, med_dose, med_directions, med_end_date, "
                              "comment, rxcui) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        key=[session['patient_id'], med_name, med_dose, med_directions, end_date, comment, rxcui]
                    )

                    # Shows a message that medication has been added, and redirects to medmain
                    flash("Medication has been added")
                    return redirect(url_for("profile.medmain"))

                except ValueError:
                    flash("The medication strength entered does not exist.")

            # A value of 0 means there is no match for the medication name
            else:
                flash("The medication name entered does not exist.")

    return render_template("historical_med_add.html", form=medication_form)

@profile.route('/med_edit/<int:active_med_id>', methods=["GET", "POST"])
@login_required
def active_medication_edit(active_med_id):
    """Display the page to edit an active medication"""

    # Instantiate medication edit form into its own variable
    medication_edit_form = MedicationEditForm()

    # Store active_med_id into its own variable, which will be used in a query
    active_med_id = active_med_id

    # If the cancel button is clicked, will return to medmain page
    if medication_edit_form.cancel_btn.data:
        return redirect(url_for("profile.medmain"))

    if medication_edit_form.update_btn.data and medication_edit_form.validate():
        # Collect updated data after user clicks the Update button
        med_name = request.form['rxterms']
        med_dose = request.form['drug_strengths']
        med_directions = request.form['med_directions']
        start_date = request.form['start_date']
        comment = request.form['comment']

        # Will display a warning if medication name field is blank
        if med_name == "":
            flash("Medication name cannot be blank")

        # Will display a warning if medication strength field is blank
        elif med_dose == "":
            flash("Medication strength cannot be blank")

        else:

            # Construct url needed to send a request to RxTerms API
            url_base = "https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms="
            url_final = url_base + med_name + "&ef=STRENGTHS_AND_FORMS,RXCUIS"

            # Send a request to RxTerms API
            response = requests.get(url_final).json()

            # A value of 1 means that one exact match for the name was found
            if response[0] >= 1:

                # Create a list of doses associated with the drug name, stripped of leading white space
                list_of_doses = []
                for dose in response[2]['STRENGTHS_AND_FORMS'][0]:
                    list_of_doses.append(dose.strip())

                # Determine if the dose entered in the form matches a dose in RxTerms; if there is a match, will
                # get the rxcui which will be later used in the API
                try:
                    dose_index = list_of_doses.index(med_dose)
                    rxcui = response[2]['RXCUIS'][0][dose_index]

                    # Add new medication entry to the database
                    query_change(
                        query="UPDATE active_med SET med_name = (?), med_dose = (?), med_directions = (?), "
                              "med_start_date = (?), comment = (?), rxcui = (?) WHERE active_med_id = (?)",
                        key=[med_name, med_dose, med_directions, start_date, comment, rxcui, active_med_id]
                    )

                    # Shows a message that medication has been updated, and redirects to medmain
                    flash("Medication has been updated")
                    return redirect(url_for("profile.medmain"))

                except ValueError:
                    flash("The medication strength entered does not exist.")

            # A value of 0 means there is no match for the medication name
            else:
                flash("The medication name entered does not exist.")

    # Retrieve the medication information using the active_med_id
    result = query_select(
        query="SELECT med_name, med_dose, med_directions, med_start_date, comment FROM active_med WHERE "
              "active_med_id = (?)",
        key=active_med_id
    )

    # Prefills the form with the medication information obtained from SQLite
    medication_edit_form.med_directions.data = result[0][2]
    start_date = result[0][3]

    # Need to convert date from a string to a date object before inserting into the form, which is a DateField
    if start_date is None:
        medication_edit_form.start_date.data = ""
    else:
        medication_edit_form.start_date.data = datetime.strptime(result[0][3], '%Y-%m-%d').date()

    medication_edit_form.comment.data = result[0][4]

    return render_template("active_med_edit.html", form=medication_edit_form, med_name=result[0][0],
                           med_dose=result[0][1])


@profile.route('/med_delete/<int:active_med_id>', methods=["GET", "POST"])
@login_required
def active_medication_delete(active_med_id):
    """Delete the selected medication"""

    # Instantiate delete medication form into its own variable
    delete_medication_form = MedicationDeleteForm()

    # Retrieve the med name and med dose using the active_med_id, and store the results in its own variable
    result = query_select(
        query="SELECT med_name, med_dose FROM active_med WHERE active_med_id = (?)",
        key=active_med_id
    )
    med_name = result[0][0]
    med_dose = result[0][1]

    # Will delete entry from the database if the confirm button is clicked
    if delete_medication_form.confirm_btn.data:
        query_change(
            query="DELETE FROM active_med WHERE active_med_id = (?)",
            key=str(active_med_id)
        )

        flash("Medication entry has been deleted")
        return redirect(url_for("profile.medmain"))

    # Clicking the cancel button will redirect to medmain
    if delete_medication_form.cancel_btn.data:
        return redirect(url_for("profile.medmain"))

    return render_template("confirm_delete.html", form=delete_medication_form, med_name=med_name, med_dose=med_dose)


@profile.route('/medication_medline/<rxcui>', methods=["GET", "POST"])
def medication_medline(rxcui):
    """Will redirect to Medline, which contains information about the specific medication based on the rxcui value"""

    base_url = "https://connect.medlineplus.gov/application?mainSearchCriteria.v.cs=2.16.840.1.113883.6.88&mainSearchCriteria.v.c="
    return redirect(base_url + rxcui)
