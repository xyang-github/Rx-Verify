# Source: https://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing-and-displaying-data/
from flask_table import Table, Col, LinkCol


class Active_Medications_Table(Table):
    """Table used to display active medications"""
    classes = ['class1']
    active_med_id = Col('med_id', show=False)
    patient_id = Col('patient_id', show=False)
    med_name = Col('Medication Name')
    med_dose = Col('Medication Strength')
    med_directions = Col('Directions')
    med_start_date = Col('Date Started')
    comment = Col('Comment')
    rxcui = Col('rxcui', show=False)
    edit = LinkCol('', 'profile.active_medication_edit', url_kwargs=dict(active_med_id='active_med_id'),
                   anchor_attrs={'class': 'edit_link'})
    delete = LinkCol('', 'profile.active_medication_delete', url_kwargs=dict(active_med_id='active_med_id'),
                     anchor_attrs={'class': 'delete_link'})
    medline = LinkCol('', 'profile.medication_medline', url_kwargs=dict(rxcui='rxcui'),
                      anchor_attrs={'class': 'medline_link'})


class Historical_Medications_Table(Table):
    """Table used to display historical medications"""
    classes = ['class1']
    active_med_id = Col('med_id', show=False)
    patient_id = Col('patient_id', show=False)
    med_name = Col('Medication Name')
    med_dose = Col('Medication Strength')
    med_directions = Col('Directions')
    med_end_date = Col('Date End')
    comment = Col('Comment')
    rxcui = Col('rxcui', show=False)

