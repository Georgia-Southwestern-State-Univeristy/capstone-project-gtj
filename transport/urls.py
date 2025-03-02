from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_transport, name='search_transport'),
    path('api/stations/', views.get_transit_stations, name='transit_stations'),
    path('api/routes/', views.get_routes, name='transit_routes'),
]