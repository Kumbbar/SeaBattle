from django.shortcuts import redirect, render
import battle
from battle.models import Gamer, Game
from .logic import get_gamer


def not_in_game(func):
    """Close urls and redirect to battlefield if user in game"""
    def wrapper(request, *args):
        gamer = get_gamer(request)
        try:
            game = Game.objects.get(player1=gamer)
            return redirect('battle:game_user1')
        except battle.models.Game.DoesNotExist:
            pass
        try:
            game = Game.objects.get(player2=gamer)
            return redirect('battle:game_user2')
        except battle.models.Game.DoesNotExist:
            pass
        return func(request, *args)
    return wrapper


def game_not_found_redirect(func):
    def wrapper(request):
        global game1_not_found, game2_not_found
        game1_not_found, game2_not_found = False, False
        gamer = get_gamer(request)
        try:
            game = Game.objects.get(player1=gamer)
        except battle.models.Game.DoesNotExist:
            game1_not_found = True
        try:
            game = Game.objects.get(player2=gamer)
        except battle.models.Game.DoesNotExist:
            game2_not_found = True

        if game1_not_found and game2_not_found:
            return redirect('battle:game_not_found')

        return func(request)
    return wrapper

