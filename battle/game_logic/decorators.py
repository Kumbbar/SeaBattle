from django.shortcuts import redirect, render
import battle
from battle.models import Gamer, Game
from .logic import get_gamer


def not_in_game(func):
    """Close urls and redirect to battlefield if user in game"""
    def wrapper(request):
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
        return func(request)
    return wrapper


def lose_redirect_player1(func):
    def wrapper(request):
        gamer = get_gamer(request)
        try:
            game = Game.objects.get(player1=gamer)
        except battle.models.Game.DoesNotExist:
            return render(request, 'battle/lose_page.html', {'gamer': gamer})
        return func(request)

    return wrapper
