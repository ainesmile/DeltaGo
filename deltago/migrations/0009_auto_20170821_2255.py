# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-21 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0008_auto_20170807_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='stockcode',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='was_price',
        ),
        migrations.RemoveField(
            model_name='details',
            name='claim',
        ),
        migrations.RemoveField(
            model_name='details',
            name='nutrition',
        ),
        migrations.AddField(
            model_name='details',
            name='claims',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='health_star_rating',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='made_in',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='nutritions',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='serving_size',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='servings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='details',
            name='weight',
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='special_price',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='endorsement',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='pic_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]