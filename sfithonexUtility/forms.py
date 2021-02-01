# https://www.ordinarycoders.com/blog/article/using-django-form-fields-and-widgets
# https://docs.djangoproject.com/fr/3.1/topics/forms/
# https://docs.djangoproject.com/en/3.0/topics/forms/formsets/
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
from django import forms
from django.db.models import Q

from .models import CustomUser


class SapeurControlVehiclesForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    resp_control = forms.ModelChoiceField(
        label='resp_control',
        queryset=CustomUser.objects.all(),
        initial=0
    )

    sap_tonne = forms.ModelChoiceField(
        label='sap_tonne',
        queryset=CustomUser.objects.filter(formation__contains='C'),
        initial=0
    )
    sap_renault = forms.ModelChoiceField(
        label='sap_renault',
        queryset=CustomUser.objects.filter(formation__contains='C'),
        initial=0
    )

    sap_mercedes = forms.ModelChoiceField(
        label='sap_mercedes',
        queryset=CustomUser.objects.filter(formation__contains='C'),
        initial=0
    )

    sap_mitsubishi = forms.ModelChoiceField(
        label='sap_mitsubishi',
        queryset=CustomUser.objects.filter(Q(formation='B') | Q(formation='C')),
        initial=0
    )


