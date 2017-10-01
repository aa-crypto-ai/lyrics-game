from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from room.models import Entry, Game, Room
from player.models import Player

from tables import RoomTable, GameTable

def play_view(request, game_id):

    game_id = int(game_id)
    game = Game.objects.get(id=game_id)
    room = game.room
    song = game.song
    entries = Entry.objects.filter(game=game)

    return render(request, 'templates/room/play.html', {
        'room': room,
        'game': game,
        'song': song,
        'entries': entries,
    })

def room_view(request, room_id):

    room = Room.objects.get(id=room_id)
    games = room.games.all().order_by('id')
    table = GameTable(games)

    return render(request, 'templates/room/view.html', {
        'room': room,
        'table': table,
    })

def list_view(request):
    player = Player.objects.get(username=request.user.username)
    rooms = Room.objects.filter(players=player)
    table = RoomTable(rooms)

    return render(request, 'templates/room/list.html', {
        'rooms': rooms,
        'table': table,
    })