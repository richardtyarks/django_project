from django.urls import path
from . import views
from .views import redirect_view

urlpatterns = [

    path('', views.index, name='index'),
    path('redirect/', redirect_view),
    path('alarmes/', views.alarm_list, name='alarm_list'),
    path('login/', views.connexion, name='connexion'),
    path('control', views.vehicles_control_create, name='control_create'),
    path('control_sapeur/', views.vehicles_control_view, name='control_sapeur'),

]
