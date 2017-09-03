# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 10:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(max_length=70)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Time Created')),
                ('end_timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Time ended')),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LyricsSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=20)),
                ('section_position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LyricsWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lyric_position', models.IntegerField()),
                ('word', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('label', models.SlugField(unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date Created')),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('lyrics', models.CharField(max_length=1000)),
                ('language', models.CharField(max_length=3)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date Added')),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='singer',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singers', to='lyrics.Song'),
        ),
        migrations.AddField(
            model_name='lyricsword',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lyrics_words', to='lyrics.Song'),
        ),
        migrations.AddField(
            model_name='lyricssection',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lyrics_sections', to='lyrics.Song'),
        ),
        migrations.AddField(
            model_name='game',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='lyrics.Room'),
        ),
        migrations.AddField(
            model_name='game',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='lyrics.Song'),
        ),
        migrations.AddField(
            model_name='entry',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='lyrics.Song'),
        ),
    ]