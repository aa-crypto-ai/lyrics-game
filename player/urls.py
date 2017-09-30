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
from django.contrib.auth.views import password_change, password_change_done
from django.contrib.auth.decorators import login_required

from player import views as player_view

urlpatterns = [
    url(r'^edit/$', login_required(player_view.update_profile), name='edit_profile'),
    url(r'^password/change/$', password_change, {'template_name': 'registration/password_change_form.html'}, name='password_change_form'),
    url(r'^password/change/done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
]