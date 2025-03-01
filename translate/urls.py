from django.urls import path
from . import views

app_name = 'translate'

urlpatterns = [
    path('', views.translate_page, name='translator'),
    path('api/translate/', views.translate_api, name='translate_api'),
    path('api/detect/', views.detect_language, name='detect_language'),
]