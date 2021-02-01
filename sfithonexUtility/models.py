# https://docs.djangoproject.com/fr/3.1/topics/auth/customizing/
# https://stackoverflow.com/questions/10147979/django-user-access-in-manytomany-field
# https://tech.serhatteker.com/post/2020-01/email-as-username-django/
from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Alarm(models.Model):
    date_time = models.DateTimeField(blank=False, null=False, default=timezone.now)
    type = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.type

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def yearpublished(self):
        return str(self.date_time)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, grade, formation, name, family_name, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, grade=grade, formation=formation, name=name,
                          family_name=family_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    grade = models.CharField(max_length=100)
    formation = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['grade', 'formation', 'name', 'family_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class Vehicle(models.Model):
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self):
        return self.name


class Controle(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')
    date = models.DateTimeField(blank=False, null=False)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self):
        return str(self.date)

    def find_resp_control(self):
        return self.user_id


class ControlDetail(models.Model):
    objects = None
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sapeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    control = models.ForeignKey(Controle, on_delete=models.CASCADE)

    def return_all_data_control(self):
        return [self.vehicle, self.sapeur, self.control]


def add_control(formset):
    for form in formset:
        date_control = form.cleaned_data['date']
        resp_control = form.cleaned_data['resp_control']
        sap_tonne = form.cleaned_data['sap_tonne']
        sap_renault = form.cleaned_data['sap_renault']
        sap_mercedes = form.cleaned_data['sap_mercedes']
        sap_mitsubishi = form.cleaned_data['sap_mitsubishi']

        control_created = Controle.objects.create(user_id=resp_control, date=date_control)
        ControlDetail(vehicle=Vehicle.objects.get(name="TONNE-POMPE"), sapeur=sap_tonne,
                      control=control_created).save()
        ControlDetail(vehicle=Vehicle.objects.get(name="PORTE-BERCE"), sapeur=sap_renault,
                      control=control_created).save()
        ControlDetail(vehicle=Vehicle.objects.get(name="TRANSPORT"), sapeur=sap_mercedes,
                      control=control_created).save()
        ControlDetail(vehicle=Vehicle.objects.get(name="SUPPORT"), sapeur=sap_mitsubishi,
                      control=control_created).save()
