# battle/urls.py

from django.urls import path
from .views import home_page, create_character_view

urlpatterns = [
    path('', home_page, name='home'),
    path('', create_character_view, name='create_character_view')
]