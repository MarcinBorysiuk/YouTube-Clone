from django.db import models
from django.contrib.auth.models import AbstractUser

class Channel(AbstractUser):
    picture = models.ImageField(upload_to='channel-pictures',null=True)

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return '/static/images/channel-pictures/no-channel-picture.jpg'

class Video(models.Model):
    title = models.CharField(max_length=60)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True)
    views = models.IntegerField(default=0)
    uploaded = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos', null=True)
