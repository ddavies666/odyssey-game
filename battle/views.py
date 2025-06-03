from django.shortcuts import render, redirect, get_object_or_404
from .forms import CharacterForm
from .models import Character
# Create your views here.


def home_page(request):
    return render(request, "battle/home.html")


def start_journey_view(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    return render(request, 'battle/start_journey.html', {'character': character})


def create_character_view(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save()
            return redirect('start_journey_view', character_id=character.id)  
    else:
        form = CharacterForm()

    return render(request, 'battle/character_customisation.html', {'form': form})
