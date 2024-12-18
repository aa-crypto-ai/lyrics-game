from django.utils import timezone
from django.db import models
from django.db.models import Max
from player.models import Player
from lyrics.models import Song

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    timestamp = models.DateTimeField('Date Created', default=timezone.now)
    status = models.CharField(max_length=10)
    players = models.ManyToManyField(Player)
    owner = models.ForeignKey(Player, related_name='rooms')

    def get_players_length(self):
        return self.players.count()

    def get_games_length(self):
        return self.games.count()

    def __unicode__(self):
        return '%s - %s' % (self.label, self.name)

class Game(models.Model):
    start_timestamp = models.DateTimeField('Time Created', default=timezone.now)
    end_timestamp = models.DateTimeField('Time ended', default=timezone.now)
    room = models.ForeignKey(Room, related_name='games')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='games')
    status = models.CharField(max_length=10, default='active')

    def get_last_played(self):
        return self.entries.all().aggregate(Max('timestamp'))['timestamp__max']

    def __unicode__(self):
        return u'%s in Room %s' % (self.song, self.room)

class Entry(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='entries')
    entry = models.CharField(max_length=70)
    timestamp = models.DateTimeField(default=timezone.now)
    player = models.ForeignKey(Player, null=True, related_name='entries')
    # specify if the entry is correct / guessed by other players
    guessed = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'entry': self.entry, 'timestamp': self.formatted_timestamp}

    def __unicode__(self):
        return u'%s: %s (%s)' % (self.game, self.entry, self.player)

class Activity(models.Model):
    name = models.SlugField(max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="activities")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="activities")

    timestamp = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - Player %s - Game %d - %s' % (self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), self.player, self.game.id, self.name)