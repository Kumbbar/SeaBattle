from django.shortcuts import render, redirect
import battle
from battle.models import Gamer, Game


def back1(request):
    """back to main menu for first player and delete all model"""
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    gamer.in_lobby = 0
    gamer.save()

    delete_game(request, gamer)
    return redirect('battle:index')


def back2(request):
    """Back to main menu for second player and delete him from game model"""
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    gamer.in_lobby = 0
    gamer.save()

    game = Game.objects.get(player2=gamer)
    game.player2 = None
    return redirect('battle:index')


def delete_game(request, gamer):
    """Delete gamer room, gamer = Gamer.objects.get(user_id=user.id)"""
    try:

        game = Game.objects.get(player1=gamer)
        game.delete()
    except battle.models.Game.DoesNotExist:
        pass


def start_battle_user(request):
    """Get gamer object - now user in game"""
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    gamer.in_lobby = 0
    gamer.in_game = 1
    gamer.save()
    return gamer


def prepare_game(request):
    """Get gamer object - now user in lobby"""
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    gamer.in_lobby = 1
    gamer.save()
    return gamer
