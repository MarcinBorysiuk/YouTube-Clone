from django.contrib import admin
from .models import Video, Channel, Comment, Reply

admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Reply)