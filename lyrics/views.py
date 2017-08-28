from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django import forms

import re
import pytz, datetime

def room_view(request, room_id):

    return render(request, 'templates/lyrics/room.html', {
        'room_id': int(room_id),
    })