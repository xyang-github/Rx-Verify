from flask import render_template, redirect, url_for, flash, request, session
from app import interaction
from app.interaction.forms import DrugInteractionForm
from . import interaction
import requests

dict_of_meds_name_rxcui = {}
list_of_med_name = []


@interaction.route('/interaction', methods=["GET", "POST"])
def interaction_main():
    interaction_form = DrugInteractionForm()
    interaction_list = list()

    # When the add button is clicked, will store the drug name and its rxcui as a dictionary in a list
    if interaction_form.btn_add.data:
        med_name = request.form['rxterms']

        if med_name == "":
            flash("Medication name cannot be blank")
        else:

            # Create a dictionary of med name and its rxcui
            dict_of_meds_name_rxcui[med_name] = get_rxcui(med_name)

            # Add med name to the med name list if it's not already there
            if med_name not in list_of_med_name:
                list_of_med_name.append(med_name)

    # If the remove button is clicked, will remove the selected med name
    if interaction_form.btn_remove.data:
        remove_med = request.form['med_list']
        list_of_med_name.remove(remove_med)

    # If the submit button is clicked, will show results or an error message
    if interaction_form.btn_submit.data:

        if len(list_of_med_name) < 2:
            flash("Must select at least two medications to run an interaction")
        else:

            # Contains a list of rxcui, which will be used in the web api
            list_of_rxcui = []

            # Get a list of rxcui from the list of medication names
            for med in list_of_med_name:
                list_of_rxcui.append(dict_of_meds_name_rxcui[med])

            drug_string = '+'.join(list_of_rxcui)

            # Construct request url
            url_base = "https://rxnav.nlm.nih.gov"
            url_final = url_base + "/REST/interaction/list.json?rxcuis=" + drug_string + "&sources=" + "drugbank"

            # Send a request to API
            response = requests.get(url_final).json()

            # Getting the drug names, interaction severity and description
            # Each interactionPair dictionary will contain a list. Each element of the list will contain a severity
            # and description.
            for interaction in response['fullInteractionTypeGroup'][0]['fullInteractionType']:
                interaction_list.append(
                    [interaction['interactionPair'][0]['interactionConcept'][0]['sourceConceptItem']['name'],
                     interaction['interactionPair'][0]['interactionConcept'][1]['sourceConceptItem']['name'],
                     interaction['interactionPair'][0]['severity'],
                     interaction['interactionPair'][0]['description']]
                )

    return render_template("interaction.html", form=interaction_form, list=list_of_med_name, result=interaction_list)


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
