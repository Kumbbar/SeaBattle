from django.shortcuts import render, redirect
from .game_logic.logic import back1, back2, start_battle_user, prepare_game, get_gamer, delete_game
from .game_logic.decorators import not_in_game, game_not_found_redirect
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
def create_game(request):
    """Create user game if he haven't game room"""
    if request.method == 'GET':
        user = request.user
        gamer = prepare_game(request)
        try:
            game = Game.objects.get(player1=gamer)
            if game.battlefield_player1 is not None:
                return redirect('battle:game_user1')
        except battle.models.Game.DoesNotExist:
            game = Game()
            game.player1 = gamer
            game.room_name = user.username
            game.save()
        return render(request, "battle/create_game.html")


def join_game(request, room_name):
    """Add user to model player2"""
    gamer = prepare_game(request)
    if request.method == 'GET':
        try:
            game = Game.objects.get(player2=gamer)
            if game.battlefield_player2 is not None:
                return redirect('battle:game_user2')
        except battle.models.Game.DoesNotExist:
            game = Game.objects.get(room_name=room_name)
            game.player2 = gamer
            game.save()
        return render(request, "battle/join_game.html")


@login_required
@game_not_found_redirect
def game_user1(request):
    """Get user1 battlefield from ajax as str and add it to model battlefield 1 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player1=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        if battlefield is None:
            return redirect('battle:create_game')
        if game.battlefield_player1 is None:
            game.battlefield_player1 = battlefield
        game.save()
    return render(request, 'battle/game_user1.html', {'game': game})


@login_required
@game_not_found_redirect
def game_user2(request):
    """Get user2 battlefield from ajax as str and add it to model battlefield 2 field"""
    gamer = start_battle_user(request)
    game = Game.objects.get(player2=gamer)
    if request.method == 'POST':
        battlefield = request.POST.get('battlefield')
        if game.battlefield_player2 is None:
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
    gamer.games += 1
    gamer.wins += 1
    gamer.save()
    return render(request, 'battle/win_page.html', {'gamer': gamer})


@game_not_found_redirect
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


@game_not_found_redirect
def surrender(request):
    """Delete the game"""
    gamer = get_gamer(request)
    # Get user and his role
    try:
        game = Game.objects.get(player1=gamer)
        player1 = True
    except battle.models.Game.DoesNotExist:
        player1 = True
        game = Game.objects.get(player2=gamer)
        player1 = False

    # Add one game if first user surrender when second user join to game
    if player1:
        if game.player2 is not None:
            gamer.games += 1
    else:
        gamer.games += 1
    game.delete()
    gamer.save()
    return redirect('battle:index')


def check_user_game(request):
    """Check game for reset localstorage in index page JS"""
    gamer = get_gamer(request)
    try:
        game = Game.objects.get(player1=gamer)
        return HttpResponse("true")
    except battle.models.Game.DoesNotExist:
        try:
            game = Game.objects.get(player2=gamer)
            return HttpResponse("true")
        except battle.models.Game.DoesNotExist:
            return HttpResponse('false')



