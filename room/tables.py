import django_tables2 as tables
from django_tables2 import A

from room.models import Room, Game

class RoomTable(tables.Table):

    n_players = tables.Column(accessor='get_players_length', verbose_name='No. of Players')
    n_games = tables.Column(accessor='get_games_length', verbose_name='No. of Games')
    id = tables.LinkColumn('room_view', text=lambda record: str(record.id), args=[A('id')])

    class Meta:
        model = Room
        sequence = ('id', 'name', 'owner', 'n_players', 'n_games', 'status')
        exclude = ('label')
        orderable = False

    def render_owner(self, record):
        return record.owner.nickname

class GameTable(tables.Table):

    start_timestamp = tables.Column(verbose_name='Time Created')
    id = tables.LinkColumn('game_play', text=lambda record: str(record.id), args=[A('room.id'), A('id')])
    last_played = tables.Column(accessor='get_last_played', verbose_name='Last Played')

    class Meta:
        model = Game
        sequence = ('id', 'status', 'start_timestamp', 'last_played')
        exclude = ('end_timestamp', 'room', 'song')
        orderable = False