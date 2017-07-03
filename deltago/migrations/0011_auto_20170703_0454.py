# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-03 04:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0010_auto_20170703_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='babycare',
            name='stockcode',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='babycaredetails',
            name='stockcode',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='babycaredetails',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]