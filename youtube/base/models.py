from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import get_video_length

class Channel(AbstractUser):
    picture = models.ImageField(upload_to='channel-pictures',null=True)
    subscriptions = models.ManyToManyField('Channel', blank=True, related_name='channel_subscribers')
    subscribers = models.ManyToManyField('Channel', blank=True, related_name='channel_subscriptions')

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return '/static/images/channel-pictures/no-channel-picture.jpg'

    def get_subscribers_count(self):
        return self.subscribers.all().count()

    def is_subscribing(self, channel):
        return channel in self.subscribers.all()


        
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

    def get_comments_count(self):
        return self.comments.count()

    def add_one_view(self):
        self.views += 1
        self.save()


class Comment(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Channel, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def get_replies_count(self):
        return self.replies.all().count()


class Reply(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Channel, related_name='reply_likes')

    def total_likes(self):
        return self.likes.count()

    
