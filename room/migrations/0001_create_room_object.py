# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 11:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lyrics', '0004_auto_20170903_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(max_length=70)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='lyrics.Song')),
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
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('label', models.SlugField(unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Date Created')),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='room.Room'),
        ),
        migrations.AddField(
            model_name='game',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='lyrics.Song'),
        ),
    ]
