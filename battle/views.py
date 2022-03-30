from django.shortcuts import render, redirect
from .game_logic.logic import back1, back2, start_battle_user, prepare_game
import battle
from .models import Gamer, Game
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User


@login_required()
def index(request):
    """Create main menu and delete button 'Create game' if user have a game"""
    gamer = Gamer.objects.get(user_id=request.user.id)
    games = Game.objects.filter(player2=None).order_by('user_id')
    user_games = len(Game.objects.all().filter(player1=gamer))
    if request.method == 'GET':
        return render(request, 'battle/index.html', {'games': games, 'user_games': user_games})


# def ajax(request):
#     if request.POST:
#         user = request.user
#         gamer = Gamer.objects.get(user_id=user.id)
#         gamer.in_lobby = 1
#         gamer.save()
#
#         try:
#             Game.objects.get(player1=gamer)
#         except battle.models.Game.DoesNotExist:
#             game = Game()
#             game.player1 = gamer
#             game.room_name = user.username
#             game.save()
#             return HttpResponse('ok')


@login_required()
def create_game(request):
    """Create user game if he haven't game room"""
    if request.method == 'GET':
        user = request.user
        gamer = Gamer.objects.get(user_id=user.id)
        gamer.in_lobby = 1
        gamer.save()

        try:
            Game.objects.get(player1=gamer)
        except battle.models.Game.DoesNotExist:
            game = Game()
            game.player1 = gamer
            game.room_name = user.username
            game.save()
        return render(request, "battle/create_game.html")


def join_game(request, room_name):
    """Add user to model player2"""
    if request.method == 'GET':
        gamer = prepare_game(request)
        game = Game.objects.get(room_name=room_name)
        game.player2 = gamer
        game.save()
        return render(request, "battle/join_game.html")


def game_user1(request):
    """Get user1 battlefield from ajax as str and add it to model battlefield 1 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player1=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        game.battlefield_player1 = battlefield
        game.save()
    return render(request, 'battle/game_user1.html', {'game': game})


def game_user2(request):
    """Get user2 battlefield from ajax as str and add it to model battlefield 2 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player2=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        game.battlefield_player2 = battlefield
        game.save()
    return render(request, 'battle/game_user2.html')


def play_game_user1(request):
    if request.method == "GET":
        pass
    else:
        pass


def play_game_user2(request):
    if request.method == "GET":
        pass
    else:
        pass


def back_player1(request):
    return back1(request)


def back_player2(request):
    return back2(request)
