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

from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.shortcuts import redirect

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^room/', include('room.urls')),
    url(r'^lyrics/', include('lyrics.urls')),
    url(r'^player/', include('player.urls')),
    url(r'^.*$', RedirectView.as_view(pattern_name='room', permanent=False), name='index'),
]
