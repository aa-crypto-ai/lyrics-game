from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django import forms

import re
import pytz, datetime

def play_view(request, room_id):

    return render(request, 'templates/lyrics/play.html', {
        'room_id': int(room_id),
    })