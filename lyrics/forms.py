from django import forms

class LyricsForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    singers = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    year = forms.CharField(widget=forms.TextInput(attrs={'size': 55}))
    lyrics = forms.CharField(widget=forms.Textarea(attrs={'rows': 35, 'cols': 65}))