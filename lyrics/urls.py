"""multichat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.http import HttpResponse

#from multichat.routing import channel_routing
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from lyrics import views as lyrics_view

urlpatterns = [
    url(r'^all/$', lyrics_view.all_songs_view),
    url(r'^import/$', lyrics_view.import_lyrics_view),
    url(r'^song/(?P<song_id>[0-9]+)/$', lyrics_view.song_view),
    url(r'^test/(?P<room_id>[0-9]+)/$', lyrics_view.play_view),
]
