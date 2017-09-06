from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from room.models import Room, Entry

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