import os
import re
import json
from datetime import datetime

import django
django.setup()

from player.models import Player
from lyrics.models import Song
from lyrics.db_manage import separate_lyrics, import_lyrics_to_db
import click

@click.command()
@click.option('--username')
@click.option('--format')
@click.option('--path')
def import_lyrics(username, format, path):

    player = Player.objects.get(username=username)
    if format not in ['kkbox']:
        raise Exception('format not supported')
    for filename in os.listdir(path):
        # filename = '54.json'
        with open(os.path.join(path, filename)) as f:
            data = json.load(f)
        
        cleaned_data = clean_data(data, format=format)
        import_lyrics_to_db(cleaned_data['lyrics'], cleaned_data['singer'], cleaned_data['year'], cleaned_data['name'], player)
        print 'done: %s' % filename

def clean_data(data, format):
    if format not in ['kkbox']:
        raise Exception('format not supported')

    cleaned_data = {}

    if format == 'kkbox':
        singer = data['singer']
        cleaned_singer = re.search('(.+?)(?=\()', singer)
        if cleaned_singer is None:
            cleaned_singer = singer
        else:
            cleaned_singer = cleaned_singer.group(0).strip()
        cleaned_data['singer'] = cleaned_singer

        name = data['name']
        cleaned_data['name'] = name.strip()

        # "2017-09-15T00:00:00+08:00"
        time = data['time']
        year = int(datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+08:00').strftime('%Y'))
        cleaned_data['year'] = year


        lyrics = data['lyrics']
        for c in [u'\u300C', u'\u300d', '(', ')', u'\uFF08', u'\uFF09', ',', '.', '~', '*', '-', 'J:', 'K:', u'\u7537:', u'\u5973:', u'\u5408:', u'\uFF5E']:
            lyrics = [phrase.replace(c, ' ') for phrase in lyrics]
        cleaned_lyrics = separate_lyrics(lyrics, format=format)
        cleaned_data['lyrics'] = cleaned_lyrics

    return cleaned_data

if __name__ == '__main__':

    import_lyrics()