# transport/urls.py

from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.home, name='home'),
    path('search-transport/', views.search_transport, name='search_transport'),
    path('routes/', views.get_routes, name='transport_routes'),
    path('stations/', views.get_transit_stations, name='transport_stations'),
]