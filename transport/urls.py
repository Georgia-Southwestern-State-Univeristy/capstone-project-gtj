from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.home, name='home'),
    path('ride/', views.ride_request, name='ride_request'), 
    path('confirmation/', views.ride_confirmation, name='ride_confirmation'),
    path('ride-list/', views.ride_list, name='ride_list'),
]