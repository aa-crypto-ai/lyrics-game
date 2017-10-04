from django.shortcuts import render
from django.db.models import Max, Q

from room.models import Entry, Room, Game, Activity
from player.models import Player

from yattag import Doc
from itertools import groupby


def process_entry(word, game_id, user_id):

    if not word.strip():
        return None

    player = Player.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)

    guessed = (Entry.objects.filter(game=game, entry__iexact=word).count() > 0)

    lyrics = game.song.lyrics_words.filter(word__iexact=word)
    positions = lyrics.values('position', 'word')
    correct = True if positions else False

    # create entry in DB
    entry = Entry.objects.create(game=game, player=player, entry=word, guessed=guessed, correct=correct)

    return {
        'positions_words': list(lyrics.values('position', 'word')),  # this is equivalent to whether the guess is correct
        'guessed': guessed,
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

    return entries.values('entry', 'player__nickname', 'guessed', 'correct')

def convert_prev_entries_to_html(prev_entries):
    doc, tag, text = Doc().tagtext()

    for entry in prev_entries:
        with tag('div', klass='entry'):
            text('%(player__nickname)s: ' % entry)
            with tag('span'):
                text('%(entry)s' % entry)
                if entry['guessed'] and entry['correct']:
                    doc.attr(klass='guessed correct')
                elif entry['guessed']:
                    doc.attr(klass='guessed')
                elif entry['correct']:
                    doc.attr(klass='correct')

    return doc.getvalue()

def save_activity_log(name, user_id, game_id):
    player = Player.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)
    activity = Activity.objects.create(name=name, player=player, game=game)

def get_connected_users(game_id):
    last_activity = Activity.objects.filter(game_id=game_id).values('player_id').annotate(last_activity=Max('timestamp')).values_list('player_id', 'last_activity')
    latest_actions = Activity.objects.filter(
        reduce(
            lambda x,y: x|y, [
                Q(player_id=player_id, timestamp=last_ts) for player_id, last_ts in last_activity
            ]
        )
    )
    active_players = latest_actions.filter(name='join').values('player_id', 'player__nickname')
    return list(active_players)