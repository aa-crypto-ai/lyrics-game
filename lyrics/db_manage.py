import re

from player.models import Player
from lyrics.models import Song, Singer, LyricsWord

def separate_lyrics(lyrics):
    lyrics_group = re.split(ur'([\u00ff-\uffff]|\S+)', lyrics);
    print len(lyrics_group), lyrics_group
    return [char.strip() for char in lyrics_group if char.strip()]

def import_lyrics(lyrics_data, singers_data, year_data, name_data, player):
    lyrics_group = separate_lyrics(lyrics_data)
    singers = [singer.strip() for singer in singers_data.split(',') if singer.strip()]
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

    for position, lyrics_word in enumerate(lyrics_group):
        lyrics_obj = LyricsWord(
            song=song,
            word=lyrics_word,
            position=position,
        )
        lyrics_obj.save()

    return True