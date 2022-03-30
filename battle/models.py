from django.db import models
from django.contrib.auth.models import User


class Gamer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    games = models.IntegerField(default=0, verbose_name='games')
    wins = models.IntegerField(default=0, verbose_name='wins')
    in_lobby = models.BooleanField(default=False, verbose_name='in_lobby')
    in_game = models.BooleanField(default=False, verbose_name='in_game')
    profile_image = models.ImageField(verbose_name='Profile_image')


class Game(models.Model):
    room_name = models.CharField(null=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    player1 = models.ForeignKey(Gamer, on_delete=models.CASCADE, related_name='gamer')
    player2 = models.ForeignKey(Gamer, on_delete=models.CASCADE, null=True)
    player1_move = models.BooleanField(default=1)
    player2_move = models.BooleanField(default=0)
    battlefield_player1 = models.TextField(max_length=1000, null=True)
    battlefield_player2 = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.player1
