from player.forms import UpdateProfileForm
from django.shortcuts import render

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