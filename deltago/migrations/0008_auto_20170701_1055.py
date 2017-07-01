# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-01 10:55
from __future__ import unicode_literals

import deltago.models.nutrition
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0007_auto_20170614_0844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='babycaredetails',
            name='babycare',
        ),
        migrations.RemoveField(
            model_name='babycaredetails',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='babycaredetails',
            name='origin',
        ),
        migrations.AddField(
            model_name='babycare',
            name='details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deltago.BabyCareDetails'),
        ),
        migrations.AlterField(
            model_name='babycaredetails',
            name='claim',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='babycaredetails',
            name='endorsement',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='babycaredetails',
            name='ingredient',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='babycaredetails',
            name='nutrition',
            field=models.TextField(blank=True, null=True, verbose_name=deltago.models.nutrition.Nutrition),
        ),
    ]
