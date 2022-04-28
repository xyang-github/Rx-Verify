from flask import render_template, flash, request, session, redirect, url_for
from flask_login import login_required

from app.interaction.forms import DrugInteractionForm
from . import interaction
import requests

from ..db.database_queries import query_select

dict_of_meds_name_rxcui = {}


@interaction.route('/interaction', methods=["GET", "POST"])
def interaction_main():
    interaction_form = DrugInteractionForm()
    interaction_list = list()

    # When the add button is clicked, will store the drug name and its rxcui as a dictionary
    if interaction_form.btn_add.data:
        med_name = request.form['rxterms']

        if med_name == "":
            flash("Medication name cannot be blank")
        else:

            # Create a dictionary of med name and its rxcui
            dict_of_meds_name_rxcui[med_name] = get_rxcui(med_name)

    # If the remove button is clicked, will remove the selected med name
    if interaction_form.btn_remove.data:
        remove_med = request.form['med_list']
        dict_of_meds_name_rxcui.pop(remove_med, None)

    # If the submit button is clicked, will show results or an error message depending on the number of meds
    if interaction_form.btn_submit.data:

        # If the checkbox to include active medications is checked, will add medication and its rxcui to the dictionary
        include_rx = request.form.get('include_rx')
        if include_rx is not None:
            active_med = query_select(
                query="SELECT med_name, rxcui FROM active_med WHERE patient_id = (?)",
                key=session['patient_id']
            )
            for med in active_med:
                dict_of_meds_name_rxcui[med[0]] = med[1]

        if len(dict_of_meds_name_rxcui) < 2:
            flash("Must enter at least two medications to run an interaction")
        else:

            drug_string = '+'.join(list(dict_of_meds_name_rxcui.values()))

            # Construct request url
            url_base = "https://rxnav.nlm.nih.gov"
            url_final = url_base + "/REST/interaction/list.json?rxcuis=" + drug_string + "&sources=" + "drugbank"

            # Send a request to API
            response = requests.get(url_final).json()

            # Getting the drug names, interaction severity and description
            # Each interactionPair dictionary will contain a list. Each element of the list will contain a severity
            # and description.
            try:
                for interaction in response['fullInteractionTypeGroup'][0]['fullInteractionType']:
                    interaction_list.append(
                        [interaction['interactionPair'][0]['interactionConcept'][0]['sourceConceptItem']['name'],
                         interaction['interactionPair'][0]['interactionConcept'][1]['sourceConceptItem']['name'],
                         interaction['interactionPair'][0]['severity'],
                         interaction['interactionPair'][0]['description']]
                    )
            except KeyError:
                interaction_list.append("There is no reported drug interaction")

        dict_of_meds_name_rxcui.clear()

    return render_template("interaction.html", form=interaction_form, list=dict_of_meds_name_rxcui,
                           result=interaction_list)


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
