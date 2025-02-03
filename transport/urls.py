from django.urls import path

from . import views

app_name = 'transport' 
urlpatterns = [
    path("", views.home, name="home"),
    path("search_locations/", views.search_locations, name="search_locations"),
]