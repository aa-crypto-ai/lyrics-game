from room.models import Room, Game, Song
from django import forms

class GameForm(forms.ModelForm):

    def __init__(self, player, data=None, *args, **kwargs):
        self.player = player

        self.room = forms.ModelChoiceField(queryset=Room.objects.filter(players=self.player), required=True, help_text="Room")
        self.song = forms.ModelChoiceField(queryset=Song.objects.filter(added_by=self.player), required=True, help_text="Song")

        super(GameForm, self).__init__(data=data, *args, **kwargs)

    class Meta:
        model = Game
        fields = ('room', 'song')
        exclude = ['start_timestamp', 'end_timestamp', 'status']

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)

        if commit:
            game.save()

        return game