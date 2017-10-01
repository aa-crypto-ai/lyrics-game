from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from lyrics.forms import LyricsForm

import re
import pytz, datetime

from lyrics.models import Song
from lyrics.db_manage import import_lyrics_to_db
from player.models import Player

@user_passes_test(lambda u: u.is_admin)
def all_songs_view(request):

    songs = Song.objects.all()

    return render(request, 'templates/lyrics/all_songs.html', {
        'songs': songs,
    })

@user_passes_test(lambda u: u.is_admin)
def song_view(request, song_id):

    song = Song.objects.get(id=song_id)

    return render(request, 'templates/lyrics/song_details.html', {
        'song': song,
    })

def import_lyrics_view(request):

    if request.method == 'POST':
        form = LyricsForm(request.POST)
        if form.is_valid():

            player = Player.objects.get(username=request.user.username)

            lyrics_data = form.cleaned_data['lyrics']
            singers_data = form.cleaned_data['singers']
            year_data = form.cleaned_data['year']
            name_data = form.cleaned_data['name']

            cleaned_lyrics = separate_lyrics(lyrics_data, format='textarea')
            success = import_lyrics_to_db(cleaned_lyrics, singers_data, year_data, name_data, player)

            if success:
                return HttpResponse('Import Song <%s>: Success' % name_data)

            return HttpResponse('Import Song <%s>: Fail' % name_data)

    else:
        form = LyricsForm()

    return render(request, 'templates/lyrics/import.html', {
        'form': form,
    })