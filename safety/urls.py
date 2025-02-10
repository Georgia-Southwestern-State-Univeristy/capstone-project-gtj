from django.urls import path
from . import views

app_name = 'safety'

urlpatterns = [
    path('', views.safety_search, name='safety_search'),
    path('results/', views.safety_results, name='safety_results'),
]