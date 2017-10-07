import argparse

import django
django.setup()

from room.models import Entry, Game

def update_entries(game_id):
    game = Game.objects.get(id=game_id)
    entries = Entry.objects.filter(game=game).order_by('timestamp')

    guessed_words = []

    for e in entries:
        entry_cleaned = e.entry.strip().lower()

        guessed = (entry_cleaned in guessed_words)
        if not guessed:
            guessed_words.append(entry_cleaned)
        e.guessed = guessed

        lyrics = game.song.lyrics_words.filter(word__iexact=entry_cleaned)
        correct = True if lyrics else False
        e.correct = correct

        e.save()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game_id", type=int)
    args = parser.parse_args()

    if args.game_id:
        games = Game.objects.filter(id=args.game_id)
    else:
        games = Game.objects.all()

    for game in games:
        print 'processing game %d' % game.id
        update_entries(game.id)