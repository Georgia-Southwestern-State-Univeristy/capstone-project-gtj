from django.urls import path

from . import views

app_name = 'transport' 
urlpatterns = [
    path("", views.transport, name="home"),
]