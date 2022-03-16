from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=40)
    picture = models.ImageField()

class Video(models.Model):
    title = models.CharField(max_length=60)
    thumbnail = models.ImageField(null=True)
    views = models.IntegerField()
    uploaded = models.DateTimeField(auto_created=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos', null=True)
