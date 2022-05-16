from django.shortcuts import render, redirect
import battle
from battle.models import Gamer, Game


def back1(request):
    """back to main menu for first player and delete all model"""
    gamer = get_gamer(request)
    gamer.in_lobby = 0
    gamer.save()

    game = Game.objects.get(player1=gamer)
    if game.battlefield_player1 is not None:
        return redirect('battle:game_user1')
    delete_game(request, gamer)
    return redirect('battle:index')


def back2(request):
    """Back to main menu for second player and delete him from game model"""
    gamer = get_gamer(request)
    gamer.in_lobby = 0
    gamer.save()

    game = Game.objects.get(player2=gamer)
    if game.battlefield_player2 is not None:
        return redirect('battle:game_user2')
    game.player2 = None
    game.save()
    return redirect('battle:index')


def delete_game(request, gamer):
    """Delete gamer room, gamer = Gamer.objects.get(user_id=user.id)"""
    try:
        game = Game.objects.get(player1=gamer)
    except battle.models.Game.DoesNotExist:
        game = Game.objects.get(player2=gamer)
    game.delete()


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


def get_gamer(request):
    user = request.user
    gamer = Gamer.objects.get(user_id=user.id)
    return gamer


def check_win_lose(request, gamer):
    try:
        game = Game.objects.get(player1=gamer)
        gamer1 = True
    except battle.models.Game.DoesNotExist:
        try:
            game = Game.objects.get(player2=gamer)
            gamer1 = False
        except battle.models.Game.DoesNotExist:
            return redirect('battle:index')
    if '1' in game.battlefield_player1 or '1' in game.battlefield_player2:
        if gamer1:
            return redirect('battle:game_user1')
        else:
            return redirect('battle:game_user2')


