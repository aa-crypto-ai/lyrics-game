from django.shortcuts import render

# from lyrics.models import Song
# from player.models import Player
from room.models import Entry, Room
from player.models import Player


def process_entry(entry, room_id, username):

    
    player = Player.objects.get(username=username)
    room = Room.objects.get(id=room_id)
    games = room.games.filter(status='active')
    if len(games) != 1:
        raise Exception('more than 1 games active')
    game = games[0]

    entry = Entry.objects.create(game=game, player=player, entry=entry)
    entry.save()

    return True

def get_guessed_lyrics(room_id):
    room = Room.objects.get(id=room_id)
    games = room.games.filter(status='active')
    if len(games) != 1:
        raise Exception('more than 1 games active')
    game = games[0]

    entries = Entry.objects.filter(game=game)

    song = game.song
    all_lyrics = song.lyrics_words.order_by('position')

    guessed_lyrics = []

    for lyrics in all_lyrics:

        guessed = False

        for e in entries.all():
            if e.entry.lower() == lyrics.word.lower():
                guessed_lyrics.append(lyrics.word)
                guessed = True
                break
        if not guessed:
            guessed_lyrics.append('----')

    return guessed_lyrics

def get_prev_entries(room_id):

    room = Room.objects.get(id=room_id)
    games = room.games.filter(status='active')
    if len(games) != 1:
        raise Exception('more than 1 games active')
    game = games[0]

    entries = Entry.objects.filter(game=game).order_by('timestamp')

    return [{'text': entry, 'username': username} for (entry, username) in entries.values_list('entry', 'player__username')]