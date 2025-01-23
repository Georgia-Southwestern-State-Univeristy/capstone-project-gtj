from django.urls import path

from . import views
app_name = 'hotels' 

urlpatterns = [
    path("", views.hotels, name="home"),
]
