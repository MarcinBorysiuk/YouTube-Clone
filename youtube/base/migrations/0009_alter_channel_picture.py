# Generated by Django 4.0.3 on 2022-03-31 20:19

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_channel_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='picture',
            field=models.ImageField(default='no-profile/no-profile.jpg', null=True, upload_to=base.models.profile_directory_path),
        ),
    ]
