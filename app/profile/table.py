from flask_table import Table, Col


class Results(Table):
    active_med_id = Col('med_id', show=False)
    patient_id = Col('patient_id', show=False)
    med_name = Col('Medication Name')
    med_dose = Col('Medication Strength')
    med_directions = Col('Directions')
    med_start_date = Col('Date Started')
    comment = Col('Comment')
    rxcui = Col('rxcui', show=False)