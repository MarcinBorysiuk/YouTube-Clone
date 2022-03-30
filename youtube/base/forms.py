from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Channel, Video


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
            attrs={'class': 'upload-view-form'}) 
        )
    
    thumbnail = forms.CharField(widget=forms.FileInput(
            attrs={'class': 'upload-view-form'}
        ))

    class Meta:
        model = Video
        fields = ['video', 'title', 'description', 'thumbnail',  'channel']
        

        