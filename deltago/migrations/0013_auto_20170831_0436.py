# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0012_commodity_pic_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='service_charge',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
