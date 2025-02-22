from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_transit, name='search_transit'),
]