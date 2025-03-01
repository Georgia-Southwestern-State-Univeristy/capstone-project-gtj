from django.urls import path
from . import views

app_name = 'currency'

urlpatterns = [
    path('', views.currency_converter, name='converter'),
    path('get-rate/', views.get_exchange_rate, name='get_rate'),
]