# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0005_auto_20170614_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babycare',
            name='price',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='babycare',
            name='special_price',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='babycare',
            name='was_price',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]