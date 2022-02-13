from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Game, Entry
from django import forms
from django.urls import reverse, reverse_lazy

class GameCreateForm(forms.ModelForm):

    class Meta:
        fields = ('name',)
        model = Game

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Game Name'

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ("entry",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["entry"].label = "Enter a Topic"

class GameLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(GameLoginForm, self).__init__(*args, **kwargs)

        username = UsernameField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
        password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'id': 'hi',
            }
    ))
