from django.shortcuts import render, redirect
from .game_logic.logic import back1, back2, start_battle_user, prepare_game, get_gamer, delete_game
from .game_logic.decorators import not_in_game, lose_redirect_player1
import battle
from .models import Gamer, Game
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse


@login_required
@not_in_game
def index(request):
    """Create main menu and delete button 'Create game' if user have a game"""
    gamer = Gamer.objects.get(user_id=request.user.id)
    games = Game.objects.filter(player2=None).order_by('user_id')
    user_games = len(Game.objects.all().filter(player1=gamer))
    if request.method == 'GET':
        return render(request, 'battle/index.html', {'games': games, 'user_games': user_games, 'gamer': gamer})


@login_required
@not_in_game
def create_game(request):
    """Create user game if he haven't game room"""
    if request.method == 'GET':
        user = request.user
        gamer = prepare_game(request)
        try:
            Game.objects.get(player1=gamer)
        except battle.models.Game.DoesNotExist:
            game = Game()
            game.player1 = gamer
            game.room_name = user.username
            game.save()
        return render(request, "battle/create_game.html")


@login_required
@not_in_game
def join_game(request, room_name):
    """Add user to model player2"""
    if request.method == 'GET':
        gamer = prepare_game(request)
        game = Game.objects.get(room_name=room_name)
        game.player2 = gamer
        game.save()
        return render(request, "battle/join_game.html")


@login_required
def game_user1(request):
    """Get user1 battlefield from ajax as str and add it to model battlefield 1 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player1=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        game.battlefield_player1 = battlefield
        game.save()
    return render(request, 'battle/game_user1.html', {'game': game})


@login_required
def game_user2(request):
    """Get user2 battlefield from ajax as str and add it to model battlefield 2 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player2=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        game.battlefield_player2 = battlefield
        game.save()
    return render(request, 'battle/game_user2.html', {'game': game})


def interact_battlefield1(request):
    """
    Get game object and return battlefield_player1 to JS
    """
    gamer = get_gamer(request)
    try:
        game = Game.objects.get(player1=gamer)
    except battle.models.Game.DoesNotExist:
        try:
            game = Game.objects.get(player2=gamer)
        except battle.models.Game.DoesNotExist:
            return redirect('battle:game_not_found')

    if request.method == "GET":
        battlefield1 = game.battlefield_player1
        return HttpResponse(battlefield1)
    else:
        battlefield = request.POST.get('battlefield')
        game.battlefield_player1 = battlefield
        game.save()
        return HttpResponse("Success")


def interact_battlefield2(request):
    """
    Get game object and return battlefield_player2 to JS
    """
    gamer = get_gamer(request)
    try:
        game = Game.objects.get(player2=gamer)
    except battle.models.Game.DoesNotExist:
        try:
            game = Game.objects.get(player1=gamer)
        except battle.models.Game.DoesNotExist:
            return redirect('battle:game_not_found')
    if request.method == "GET":
        battlefield2 = game.battlefield_player2
        return HttpResponse(battlefield2)
    else:
        battlefield = request.POST.get('battlefield')
        game.battlefield_player2 = battlefield
        game.save()
        return HttpResponse("Success")


def player_win(request):
    """add win to user and redirect to win page"""
    gamer = get_gamer(request)
    gamer.games += 1
    gamer.wins += 1
    gamer.save()
    return render(request, 'battle/win_page.html', {'gamer': gamer})


def player_lose(request):
    """delete game and redirect to lose page"""
    gamer = get_gamer(request)
    delete_game(request, gamer)
    gamer.games += 1
    gamer.save()
    return render(request, 'battle/lose_page.html', {'gamer': gamer})


def back_player1(request):
    return back1(request)


def back_player2(request):
    return back2(request)


def game_not_found(request):
    """Page if one of the players gave up"""
    return render(request, 'battle/game_not_found.html')


def surrender(request):
    """Delete the game"""
    gamer = get_gamer(request)
    try:
        game = Game.objects.get(player1=gamer)
        player1 = True
    except battle.models.Game.DoesNotExist:
        game = Game.objects.get(player2=gamer)
        player1 = False

    if player1:
        if game.player2 is None:
            return redirect('battle:index')
        else:
            gamer.games += 1
            return redirect('battle:index')
    else:
        gamer.games += 1
    game.delete()
    gamer.save()
    return redirect('battle:index')