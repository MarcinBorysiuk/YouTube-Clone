# Generated by Django 4.0.3 on 2022-03-22 20:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_channel_subscribtion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='subscribtion',
        ),
        migrations.AddField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='channel_subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='channel',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='channel_subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]