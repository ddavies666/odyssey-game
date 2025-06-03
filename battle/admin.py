from django.contrib import admin
from .models import Character, Archetype, Armour, Weapon

# Register your models here.
admin.site.register(Character)
admin.site.register(Archetype)
admin.site.register(Armour)
admin.site.register(Weapon)

