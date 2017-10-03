import re

from player.models import Player
from lyrics.models import Song, Singer, LyricsWord

def separate_lyrics(lyrics, format='textarea'):
    if format == 'textarea':
        lyrics_group = re.split(ur'([\u00ff-\uffff]|\S+)', lyrics);

        chars = []

        for char in lyrics_group:

            if char.find('\n') > -1:
                chars.append('\n')
                continue

            if char.strip():
                chars.append(char.strip())

        return chars

    if format == 'kkbox':
        chars = []
        for phrase in lyrics:
            if not phrase.strip():
                continue
            # asterisk (whole space)
            if u'\uFF0A' in phrase:
                continue
            # neglect lines with colon, these are listing names of backstage staff
            if u'\uff1a' in phrase or ':' in phrase:
                continue
            lyrics_group = re.split(ur'([\u00ff-\uffff]|\S+)', phrase);

            for char in lyrics_group:
                if char.strip():
                    chars.append(char.strip())
            chars.append('\n')

        return chars

def import_lyrics_to_db(lyrics_data, singers_data, year_data, name_data, player):
    if ',' in singers_data:
        singers = [singer.strip() for singer in singers_data.split(',') if singer.strip()]
    elif '&' in singers_data:
        singers = [singer.strip() for singer in singers_data.split('&') if singer.strip()]
    elif '/' in singers_data:
        singers = [singer.strip() for singer in singers_data.split('/') if singer.strip()]
    else:
        singers = [singers_data.strip()]

    year = int(year_data)
    name = name_data.strip()

    song = Song(
        name=name,
        year=year,
        language='yue',
        added_by=player,
    )
    song.save()

    for singer in singers:
        singer_obj = Singer(name=singer, song=song)
        singer_obj.save()

    LyricsWord.objects.bulk_create(
        [LyricsWord(song=song, word=lyrics_word, position=position) for position, lyrics_word in enumerate(lyrics_data)]
    )

    return True