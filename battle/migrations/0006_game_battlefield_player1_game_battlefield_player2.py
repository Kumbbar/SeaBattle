# Generated by Django 4.0 on 2022-03-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0005_alter_game_player2'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='battlefield_player1',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='battlefield_player2',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
