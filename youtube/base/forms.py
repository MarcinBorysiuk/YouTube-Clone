from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Channel, Video


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

class UploadVideoForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'upload-view-form', 'placeholder': 'Title for your video'}
        ),
        label=''
        )
    
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'upload-view-form', 'placeholder': 'Description (optional)'}
        ),
        label=''
        )

    video = forms.CharField(
        widget=forms.FileInput(
            attrs={'class': 'upload-view-form'}),
        label=forms.FileInput(
            attrs={'class': 'custom-file-upload'}
        )   
        )
    
    thumbnail = forms.CharField(widget=forms.FileInput(
            attrs={'class': 'upload-view-form'}
        ))

    class Meta:
        model = Video
        fields = ['video', 'title', 'description', 'thumbnail',  'channel']
        widgets = {
            'channel': forms.HiddenInput(),
            }

        