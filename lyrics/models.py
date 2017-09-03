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