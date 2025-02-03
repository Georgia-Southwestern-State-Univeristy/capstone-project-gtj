from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('country/', views.country_info, name='country_info'),
]