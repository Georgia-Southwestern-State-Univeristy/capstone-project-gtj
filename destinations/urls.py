from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('city-info/', views.city_info, name='city_info'),
]