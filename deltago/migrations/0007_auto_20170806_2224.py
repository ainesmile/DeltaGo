# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-06 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0006_comment_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reply',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
