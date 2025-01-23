from django.urls import path

from . import views

app_name = 'planes' 

urlpatterns = [
    path("", views.planes, name="home"),
]