# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-03 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0012_auto_20170703_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babycaredetails',
            name='nutrition',
            field=models.TextField(blank=True, max_length=128, null=True),
        ),
    ]
