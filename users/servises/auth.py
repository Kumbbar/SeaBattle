from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from battle.game_logic.logic import delete_game
import battle
from battle.models import Gamer, Game
from django.contrib.auth import logout


def login_user(request):
    """login user and do redirect to gamer url if he have a game"""
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # return render(request, 'battle/index.html', {'form': form})
            return redirect('battle:index')
        else:
            return render(request, 'registration/login.html', {'form': form})
    context = {'form': form}
    return render(request, 'registration/login.html', context)


def register_user(request):
    """User registration and add him to gamer model"""
    if request.method == "GET":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            gamer = Gamer()
            gamer.user_id = new_user.id
            gamer.save()
            login(request, new_user)
            return redirect('battle:index')
    return render(request, 'registration/registration.html', {'form': form})


def logged_out(request):
    """Delete gamer room if he logged out"""
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    gamer.in_lobby = 0
    gamer.save()

    try:
        delete_game(request, gamer)
        logout(request)
    except:
        pass



