from django.shortcuts import render
from django.http import HttpResponse

from django import forms

import re
import pytz, datetime

from lyrics.models import Song
from lyrics.db_manage import import_lyrics
from player.models import Player

def play_view(request, room_id):

    return render(request, 'templates/lyrics/play.html', {
        'room_id': int(room_id),
    })

# Create your views here.
def all_songs_view(request):

    songs = Song.objects.all()

    return render(request, 'templates/lyrics/all_songs.html', {
        'songs': songs,
    })

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

            success = import_lyrics(lyrics_data, singers_data, year_data, name_data, player)

            if success:
                return HttpResponse('Import Song <%s>: Success' % name_data)

            return HttpResponse('Import Song <%s>: Fail' % name_data)

    else:
        form = LyricsForm()

    return render(request, 'templates/lyrics/import.html', {
        'form': form,
    })

class LyricsForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    singers = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    year = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    lyrics = forms.CharField(widget=forms.Textarea(attrs={'rows': 35, 'cols': 65}))