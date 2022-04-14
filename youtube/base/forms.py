from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Channel


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'login-input','placeholder':'Channel Name'}),
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'login-input','placeholder':'E-mail Address'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'login-input','placeholder':'Password'}),
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'login-input','placeholder':'Confirm Password'}),
        )
    
    class Meta:
        model = Channel
        fields = ['email', 'username', 'password1', 'password2']

        

        