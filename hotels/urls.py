from django.urls import path

from . import views
app_name = 'hotels' 

urlpatterns = [
    path("", views.home, name="home"),
    path('search-cities/', views.search_cities, name='search_cities'),
    path('api-debug/', views.api_debug, name='api_debug'),
]
