from django.urls import path
from . import views

app_name = 'battle'
urlpatterns = [
    path('', views.index, name='index'),

    path('create_game/', views.create_game, name='create_game'),
    path('join_game/<str:room_name>', views.join_game, name='join_game'),


    path('back_player1/', views.back_player1, name='back_player1'),
    path('back_player2/', views.back_player2, name='back_player2'),

    path('game_user1/', views.game_user1, name='game_user1'),
    path('game_user2/', views.game_user2, name='game_user2'),

    path('interact_battlefield1/', views.interact_battlefield1, name='interact_battlefield1'),
    path('interact_battlefield2/', views.interact_battlefield2, name='interact_battlefield2')

]
