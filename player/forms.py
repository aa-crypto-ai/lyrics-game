from player.models import Player
from django import forms

class UpdateProfileForm(forms.ModelForm):
    username = forms.SlugField(required=True, disabled=True)
    email = forms.EmailField(required=True, max_length=50)
    nickname = forms.CharField(required=True, max_length=20)

    class Meta:
        model = Player
        fields = ('username', 'email', 'nickname')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and Player.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        player = super(UpdateProfileForm, self).save(commit=False)
        player.email = self.cleaned_data['email']

        if commit:
            player.save()

        return player