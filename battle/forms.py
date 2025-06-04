from django import forms
from .models import Character, User


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'nickname', 'skin_tone', 'hairstyle', 'facial_hair', 'religion', 'archetype']


