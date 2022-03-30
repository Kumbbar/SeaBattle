from django.urls import path
from . import views

app_name = 'battle'
urlpatterns = [
    path('', views.index, name='index'),

    path('create_game/', views.create_game, name='create_game'),
    path('join_game/<str:game_room_name>', views.join_game, name='join_game'),


    path('back_player1/', views.back_player1, name='back_player1'),
    path('back_player2/', views.back_player2, name='back_player2'),

    path('game_user1/', views.game_user1, name='game_user1'),
    path('game_user2/', views.game_user2, name='game_user2'),

    path('load_battlefield1/', views.load_battlefield1, name='load_battlefield1'),
    path('load_battlefield2/', views.load_battlefield2, name='load_battlefield2')

]
