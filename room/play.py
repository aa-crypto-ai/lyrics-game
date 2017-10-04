from django.shortcuts import render

from room.models import Entry, Room, Game, Activity
from player.models import Player

from yattag import Doc
from itertools import groupby


def process_entry(word, game_id, user_id):

    if not word.strip():
        return None

    player = Player.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)

    exist = (Entry.objects.filter(game=game, entry__iexact=word).count() > 0)
    entry = Entry.objects.create(game=game, player=player, entry=word)

    lyrics = game.song.lyrics_words.filter(word__iexact=word)

    return {
        'positions_words': list(lyrics.values('position', 'word')),
        'exist': exist,
    }

def get_guessed_lyrics(game_id):
    game = Game.objects.get(id=game_id)

    entries = Entry.objects.filter(game=game)

    song = game.song
    all_lyrics = song.lyrics_words.order_by('position')

    guessed_words = all_lyrics.extra(
        select={
            'entry': 'room_entry.entry',
        },
        tables=['room_entry'],
        where=['room_entry.game_id = %d AND lower(lyrics_lyricsword.word) = lower(room_entry.entry)' % game.id]
    )
    words_count = all_lyrics.count()
    line_breaks_pos = all_lyrics.filter(word='\n').values_list('position', flat=True)

    result = [''] * words_count

    def map_to_result_str(data):
        position, word = data
        result[position] = word

    map(map_to_result_str, list(guessed_words.values_list('position', 'word')))
    for pos in line_breaks_pos:
        result[pos] = '\n'

    lyrics_lines = [list(group) for k, group in groupby(result, lambda x: x == "\n") if not k]  # k is False if it matches the splitter
    return lyrics_lines

def convert_guessed_lyrics_to_html(lyrics_lines):
    """ guessed_lyrics is a list of strings, with unknown represented as '?', and line break as '\n'

        return a html string
    """

    doc, tag, text = Doc().tagtext()

    word_idx = 0

    for line_idx, line in enumerate(lyrics_lines):
        with tag('div', id='line_%d' % line_idx, klass='line'):
            for c in line:
                if c == '':
                    with tag('span', id='word_%d' % word_idx, klass='word hidden'):
                        text('?')
                else:
                    with tag('span', id='word_%d' % word_idx, klass='word'):
                        text(c)
                word_idx = word_idx + 1
            word_idx = word_idx + 1

    return doc.getvalue()

def get_prev_entries(game_id):

    game = Game.objects.get(id=game_id)

    entries = Entry.objects.filter(game=game).order_by('timestamp')

    return [{'text': entry, 'nickname': nickname} for (entry, nickname) in entries.values_list('entry', 'player__nickname')]

def convert_prev_entries_to_html(prev_entries):
    doc, tag, text = Doc().tagtext()

    for entry in prev_entries:
        with tag('div'):
            text('%(nickname)s: %(text)s' % entry)

    return doc.getvalue()

def save_activity_log(name, user_id, game_id):
    player = Player.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)
    activity = Activity.objects.create(name=name, player=player, game=game)