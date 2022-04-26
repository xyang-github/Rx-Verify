from flask import render_template, redirect, url_for, flash, request, session
from app import interaction
from app.interaction.forms import DrugInteractionForm
from . import interaction
import requests

list_of_meds = []


@interaction.route('/interaction', methods=["GET", "POST"])
def interaction_main():
    interaction_form = DrugInteractionForm()

    # When the add button is clicked, will store the drug name and its rxcui as a dictionary in a list
    if interaction_form.btn_add.data:
        med_name = request.form['rxterms']

        if med_name == "":
            flash("Medication name cannot be blank")
        else:
            list_of_meds.append((med_name, get_rxcui(med_name)))

    return render_template("interaction.html", form=interaction_form, list=list_of_meds)


def get_rxcui(med_name):
    """Returns rxcui given the medication name"""

    url_base = "https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms="
    url_final = url_base + med_name + "&ef=STRENGTHS_AND_FORMS,RXCUIS"

    # Send a request to API
    response = requests.get(url_final).json()

    # Make sure that the name chosen is from the list
    if response[0] == 1:

        # list of doses associated with the drug name, stripped of leading white space
        list_of_doses = []
        for dose in response[2]['STRENGTHS_AND_FORMS'][0]:
            list_of_doses.append(dose.strip())

    return response[2]['RXCUIS'][0][0]
