from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Channel


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'login-input','placeholder':'Password'}),
        )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'login-input','placeholder':'Confirm Password'}),
        )
    username = forms.CharField(
        label="Channel Name",
        widget=forms.TextInput(attrs={'class':'login-input','placeholder':'Channel Name'}),
        )

    class Meta:
        model = Channel
        fields = ['username', 'password1', 'password2']

        