# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-02 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0008_auto_20170701_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='babycaredetails',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
