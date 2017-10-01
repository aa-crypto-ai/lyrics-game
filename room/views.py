from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from room.models import Entry, Game, Room
from player.models import Player

from room.tables import RoomTable, GameTable
from room.forms import GameForm

def play_view(request, room_id, game_id):

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
    rooms = Room.objects.filter(players=request.user)
    table = RoomTable(rooms)

    return render(request, 'templates/room/list.html', {
        'rooms': rooms,
        'table': table,
    })

def create_game(request):

    if request.method == 'POST':

        form = GameForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            room_id = form.data['room']

            return HttpResponseRedirect(reverse('room_view', args=[room_id]))

    else:
        form = GameForm(request.user)

    return render(request, 'templates/room/create_game.html', {
        'form': form,
    })