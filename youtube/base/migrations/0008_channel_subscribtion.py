# Generated by Django 4.0.3 on 2022-03-22 19:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='subscribtion',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]