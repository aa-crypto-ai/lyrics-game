from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from room.models import Room, Entry
from player.models import Player

@login_required
def play_view(request, room_id):

    room_id = int(room_id)
    room = Room.objects.get(id=room_id)
    game = room.games.all()[0]
    song = game.song
    entries = Entry.objects.filter(game=game)

    return render(request, 'templates/room/play.html', {
        'room': room,
        'game': game,
        'song': song,
        'entries': entries,
    })

def list_view(request):
    player = Player.objects.get(username=request.user.username)
    rooms = Room.objects.filter(players=player)
    print player
    # print rooms
    print rooms[0].players.all()
    return render(request, 'templates/room/list.html', {
        'rooms': rooms,
    })