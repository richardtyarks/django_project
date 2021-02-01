# https://learndjango.com/tutorials/django-login-and-logout-tutorial
# https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
# https://docs.djangoproject.com/en/3.1/ref/forms/validation/
# https://stackoverflow.com/questions/14647723/django-forms-if-not-valid-show-form-with-error-message
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, auth
from django.forms import formset_factory
from django.shortcuts import render, redirect

from .control_formset_validation import check_formset_validation, switch_formset_validation
from .forms import SapeurControlVehiclesForm
from .models import Alarm, Controle, Vehicle, ControlDetail


def alarm_list(request):
    alarms_array = Alarm.objects.order_by('-date_time')

    def extract_year_from_alarm(list_alarms):
        list_array_year_distinct = []
        for yearAlarm in list_alarms:
            year_distinct = yearAlarm.__getattribute__('date_time').strftime("%Y")
            if year_distinct not in list_array_year_distinct:
                list_array_year_distinct.append(year_distinct)
        return list_array_year_distinct

    return render(request, 'sfithonexUtility/view_alarm.html',
                  {'years': extract_year_from_alarm(alarms_array), 'alarms': alarms_array})


def index(request):
    return render(request, 'sfithonexUtility/index.html')


@login_required(login_url='/login/')
def vehicles_control_create(request):
    if request.user.grade == "Cap" or request.user.grade == "Fourr":
        sapeur_control_vehicles_form_set = formset_factory(SapeurControlVehiclesForm, max_num=6, min_num=6)
        if request.method == 'POST':
            formset = sapeur_control_vehicles_form_set(request.POST, request.FILES)
            if formset.is_valid():
                Controle.objects.all().delete()
                list_switch = switch_formset_validation(formset, check_formset_validation(formset))
                return render(request, 'sfithonexUtility/vehicles_control.html', {'formset': formset,
                                                                                  'error': list_switch[0],
                                                                                  'error_message': list_switch[1]})
        else:
            formset = sapeur_control_vehicles_form_set()

        return render(request, 'sfithonexUtility/vehicles_control.html',
                      {'formset': formset})
    else:
        return redirect_view()


@login_required(login_url='/login/')
def vehicles_control_view(request):
    list_control = Controle.objects.order_by('date')
    list_control_resp = []
    details_control = ControlDetail.objects.order_by('control')
    tonne = Vehicle.objects.get(name='TONNE-POMPE')
    transport = Vehicle.objects.get(name='TRANSPORT')
    support = Vehicle.objects.get(name='SUPPORT')
    berce = Vehicle.objects.get(name='PORTE-BERCE')

    for control in list_control:
        list_control_resp.append(control.find_resp_control())

    return render(request, 'sfithonexUtility/view_control_vehicle.html', {'details': details_control,
                                                                          'list_control': list_control,
                                                                          'list_control_resp': list_control_resp,
                                                                          'tonne': tonne,
                                                                          'transport': transport,
                                                                          'support': support,
                                                                          'berce': berce})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                messages.info(request, "You are now logged in as {email}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    if User.is_authenticated:
        auth.logout(request)
    return render(request, 'sfithonexUtility/login.html', context={"form": form})


def redirect_view():
    response = redirect('/')
    return response
