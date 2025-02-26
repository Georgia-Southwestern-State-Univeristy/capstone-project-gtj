from django.urls import path

from . import views

app_name = 'planes' 

urlpatterns = [
    path("", views.home, name="home"),
    path('search-airports/', views.search_airports, name='search_airports'),
    path('api-debug/', views.api_debug, name='api_debug'),
]