from django.db import models
from player.models import Player
from django.utils import timezone


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    # use ISO-639-3 standard
    language = models.CharField(max_length=3)

    timestamp = models.DateTimeField('Date Added', default=timezone.now)
    added_by = models.ForeignKey(Player, null=True, related_name='songs')

    @property
    def lyrics(self):
        return ''.join([str(lyrics) for lyrics in self.lyrics_words.all().order_by('position')])

    def __unicode__(self):
        return self.name

class Singer(models.Model):
    name = models.CharField(max_length=100)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='singers')

    def __unicode__(self):
        return self.name

class LyricsWord(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="lyrics_words")
    position = models.IntegerField()
    word = models.CharField(max_length=70)

    def __unicode__(self):
        return self.word

class LyricsSection(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='lyrics_sections')
    section_name = models.CharField(max_length=20)
    section_position = models.IntegerField()

    def __unicode__(self):
        return '%s - %s - position %d' % (self.song, self.section_name, self.section_position)

class Entry(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='entries')
    entry = models.CharField(max_length=70)
    timestamp = models.DateTimeField(default=timezone.now)
    player = models.ForeignKey(Player, null=True, related_name='entries')
    # handle = models.TextField()

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'entry': self.entry, 'timestamp': self.formatted_timestamp} # 'handle': self.handle

    def __unicode__(self):
        return '%s: %s (%s)' % (self.song, self.entry, self.user)

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    timestamp = models.DateTimeField('Date Created', default=timezone.now)
    status = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s - %s' % (self.label, self.song)

# class Player(models.Model):
#     player = models.OneToOneField(User, on_delete=models.CASCADE)
#     rooms = models.ManyToManyField(Room, related_name='players')

class Game(models.Model):
    start_timestamp = models.DateTimeField('Time Created', default=timezone.now)
    end_timestamp = models.DateTimeField('Time ended', default=timezone.now)
    room = models.ForeignKey(Room, related_name='games')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='games')
    status = models.CharField(max_length=10)
    