from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import CharacterForm
from .models import Character
import random
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in after register
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'battle/register.html', {'form': form})


def home_page(request):
    return render(request, "battle/home.html")


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'battle/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'battle/home.html')


def start_journey_view(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    return render(request, 'battle/start_journey.html', {'character': character})

def village_view(request):
    return render(request, "battle/village.html")

def character_select_view(request):
    characters = Character.objects.all()
    return render(request, 'battle/character_select.html', {'characters': characters})


def create_character_view(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save()
            return redirect('start_journey_view', character_id=character.id)  
    else:
        form = CharacterForm()

    return render(request, 'battle/character_customisation.html', {'form': form})


def battle_view(request, fighter1_id, fighter2_id):
    
    fighter_1 = get_object_or_404(Character, id=fighter1_id)
    fighter_2 = get_object_or_404(Character, id=fighter2_id)

    message = None
    winner = None
    turn = request.session.get("turn", "fighter_1")

    if request.method == 'POST':
        attack_input = request.POST.get('action')
        print("ACTION RECEIVED:", attack_input)
        print("CURRENT TURN:", turn)

        if turn == "fighter_1":
            if attack_input in ["light", "normal", "heavy"]:
                dmg = fighter_1.attack(fighter_2, attack_input)
                request.session["message"] = f"{fighter_1.name} attacked {fighter_2.name} for {dmg} damage!"

            elif attack_input == "heal":
                heal_amount = fighter_1.heal(fighter_1.vitality)
                fighter_1.health += heal_amount
                request.session["message"] = f"{fighter_1.name} healed for {heal_amount} HP!"

            elif attack_input == "rest":
                stamina_recovery_amount = fighter_1.rest(fighter_1.focus)
                fighter_1.stamina += stamina_recovery_amount
                request.session["message"] = f"{fighter_1.name} rested for {stamina_recovery_amount} Stamina!"

            request.session["turn"] = "fighter_2"

        elif turn == "fighter_2":
            if attack_input == 'enemy_turn':
                attack_input = random.choice(["light", "normal", "heavy"])
                dmg = fighter_2.attack(fighter_1, attack_input)
                if fighter_2.stamina < 30:
                    fighter_2.rest(fighter_2.focus)
                print(attack_input)
                dmg = fighter_2.attack(fighter_1, attack_input)
                print(dmg)
                message = f"{fighter_2.name} attacked {fighter_1.name} for {dmg} damage!"

            request.session["turn"] = "fighter_1"

        # Save updated states
        fighter_1.save()
        fighter_2.save()

    # Check for winner
    if fighter_1.health <= 0 or fighter_2.health <= 0:
        winner = fighter_1 if fighter_2.health <= 0 else fighter_2
        loser = fighter_1 if fighter_1.health <= 0 else fighter_2
        winnings = winner.battle_winnings(loser.level)
        xp_gained = winner.gain_xp(loser.level)
        request.session["message"] = (
            f"🏆 {winner.name} wins the battle!<br>"
            f"Gold earned: {winnings}<br>"
            f"XP earned: {xp_gained}"
)
        
        fighter_1.resest_attributes()
        fighter_2.resest_attributes()
    
    

    # Reset turn and redirect to avoid post-back issues
    return render(request, 'battle/battle_view.html', {
    'fighter_1': fighter_1,
    'fighter_2': fighter_2,
    'message': request.session.pop("message", None),
    'money': request.session.pop("message", None),
    'turn': request.session.get("turn", "fighter_1")
})
