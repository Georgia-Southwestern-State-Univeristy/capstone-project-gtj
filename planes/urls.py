from django.urls import path

from . import views

app_name = 'planes' 

urlpatterns = [
    path("", views.home, name="home"),
    path('api/flights/', views.FlightDataView.as_view(), name='flight_api'),
    path('search-airports/', views.search_airports, name='search_airports'),
]