from player.models import Player
from django import forms

class UpdateProfileForm(forms.ModelForm):
    username = forms.SlugField(required=True, max_length=50)
    email = forms.EmailField(required=True, disabled=True)
    nickname = forms.CharField(required=True, max_length=20)

    class Meta:
        model = Player
        fields = ('email', 'username', 'nickname')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and Player.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        player = super(UpdateProfileForm, self).save(commit=False)
        player.username = self.cleaned_data['username']

        if commit:
            player.save()

        return player