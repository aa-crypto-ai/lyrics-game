from room.models import Room, Game, Song
from django import forms

class GameForm(forms.ModelForm):

    def __init__(self, player, data=None, *args, **kwargs):
        self.player = player

        super(GameForm, self).__init__(data=data, *args, **kwargs)
        self.fields['room'].queryset = self.fields['room'].queryset.filter(players=self.player)
        self.fields['song'].queryset = self.fields['song'].queryset.filter(added_by=self.player)

    class Meta:
        model = Game
        fields = ('room', 'song')
        exclude = ['start_timestamp', 'end_timestamp', 'status']

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)

        if commit:
            game.save()

        return game