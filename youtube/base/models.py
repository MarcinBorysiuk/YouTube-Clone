from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import get_video_length

class Channel(AbstractUser):
    picture = models.ImageField(upload_to='channel-pictures',null=True)

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return '/static/images/channel-pictures/no-channel-picture.jpg'

class Video(models.Model):
    video = models.FileField(upload_to='videos', null=True)
    title = models.CharField(max_length=60)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True)
    description = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    uploaded = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos', null=True)

    def get_length(self):
        get_video_length(self.video.url)


class Comment(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Channel, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()
