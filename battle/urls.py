# battle/urls.py

from django.urls import path
from .views import home_page, create_character_view, battle_view

urlpatterns = [
    path('', home_page, name='home'),
    path('', create_character_view, name='create_character_view'),
    path('battle/<int:fighter1_id>/<int:fighter2_id>/', battle_view, name='battle'),,

]