import django
django.setup()

from player.models import Player
import click

@click.command()
@click.option('--email', help='Number of greetings.')
@click.option('--username')
@click.option('--nickname')
@click.option('--password')
def create_user(email, username, nickname, password):
    Player.objects.create_user(email=email, username=username, nickname=nickname, password=password)

if __name__ == '__main__':

    create_user()