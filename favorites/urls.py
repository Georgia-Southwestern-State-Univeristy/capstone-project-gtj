from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.view_favorites, name='view_favorites'),
    path('add/', views.add_favorite, name='add_favorite'),
    path('remove/<int:favorite_id>/', views.remove_favorite, name='remove_favorite'),
]