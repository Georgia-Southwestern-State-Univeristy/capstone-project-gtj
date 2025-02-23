# transport/urls.py

from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.home, name='home'),
    path('options/', views.get_transport_options, name='transport_options'),
    path('routes/', views.get_routes, name='transport_routes'),
]