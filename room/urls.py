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
from django.contrib.auth.decorators import login_required

from room import views as room_view

urlpatterns = [
    url(r'^(?P<room_id>[0-9]+)/game/(?P<game_id>[0-9]+)/$', login_required(room_view.play_view), name='game_play'),
    url(r'^(?P<room_id>[0-9]+)/$', login_required(room_view.room_view), name='room_view'),
    url(r'^create_game/$', login_required(room_view.create_game), name='create_game'),
    url(r'^$', login_required(room_view.list_view), name='room'),
]
