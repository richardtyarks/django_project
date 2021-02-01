# https://www.tutorialspoint.com/count-occurrences-of-an-element-in-a-list-in-python
from sfithonexUtility.models import add_control


def check_formset_validation(forms):
    distinct_resp_control = []
    distinct_date_control = []

    for form in forms:
        resp_control = form.cleaned_data.get('resp_control')
        list_sapeur_in_control = [form.cleaned_data.get('sap_tonne'), form.cleaned_data.get('sap_renault'),
                                  form.cleaned_data.get('sap_mercedes'), form.cleaned_data.get('sap_mitsubishi')]
        date_control = form.cleaned_data.get('date')
        if resp_control in distinct_resp_control:
            return 1

        if resp_control not in list_sapeur_in_control:
            return 2

        if date_control in distinct_date_control:
            return 3

        for sapeur in list_sapeur_in_control:
            ctn_element = list_sapeur_in_control.count(sapeur)
            if ctn_element > 1:
                return 4

        distinct_resp_control.append(resp_control)
        distinct_date_control.append(date_control)
    return 5


def switch_formset_validation(formset, value_formset_validation):
    if value_formset_validation == 1:
        return [True, "Un responsable ne peut pas superviser 2 contrôles"]
    if value_formset_validation == 2:
        return [True, "Un responsable n'est pas dans un contrôle"]
    if value_formset_validation == 3:
        return [True, "Des contrôles ne peuvent pas posséder la même date"]
    if value_formset_validation == 4:
        return [True, "Un sapeur ne peut pas s'occuper de plusieurs véhicules dans un même contrôle"]
    if value_formset_validation == 5:
        add_control(formset)
        return [False, "Insertion réussi !"]
