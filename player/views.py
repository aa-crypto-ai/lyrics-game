from player.forms import UpdateProfileForm, RegistrationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from room.models import Room

def update_profile(request):

    player = request.user
    updated = False

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            updated = True
    else:
        form = UpdateProfileForm(initial={
            'username': player.username,
            'email': player.email,
            'nickname': player.nickname,
        })

    return render(request, 'templates/player/update_profile.html', {
        'form': form,
        'updated': updated,
    })

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            player = authenticate(email=email, password=raw_password)
            login(request, player)
            room = Room.objects.get(label='demo_room')
            room.players.add(player)
            return redirect('room')
    else:
        form = RegistrationForm()
    return render(request, 'templates/player/registration.html', {'form': form})