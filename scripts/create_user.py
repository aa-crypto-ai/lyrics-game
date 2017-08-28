import django
django.setup()

from django.contrib.auth.models import User
import click

@click.command()
@click.option('--username', help='Number of greetings.')
@click.option('--password')
@click.option('--email')
@click.option('--first_name')
@click.option('--last_name')
def create_user(username, password, email, first_name, last_name):
    User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

if __name__ == '__main__':

    create_user()