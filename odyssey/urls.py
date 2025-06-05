"""
URL configuration for odyssey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from battle.views import home_page, create_character_view, start_journey_view, battle_view, register_view, login_page, character_select_view, village_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_page, name='home'),
    path('character-customisation', create_character_view, name='create_character_view'),
    path('start-journey<int:character_id>/', start_journey_view, name='start_journey_view'),
    path('battle/<int:fighter1_id>/<int:fighter2_id>/', battle_view, name='battle'),
    path('register/', register_view, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('select-character/', character_select_view, name='character_select'),
    path('village/', village_view, name='village_view'),



]
