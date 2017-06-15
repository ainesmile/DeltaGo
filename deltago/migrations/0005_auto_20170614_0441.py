# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 04:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0004_auto_20170614_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='BabyCareDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=128, null=True)),
                ('origin', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pic_url', models.URLField(blank=True, null=True)),
                ('ingredient', models.TextField(blank=True, null=True)),
                ('claim', models.TextField(blank=True, null=True)),
                ('endorsement', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='babycare',
            name='claim',
        ),
        migrations.RemoveField(
            model_name='babycare',
            name='details',
        ),
        migrations.RemoveField(
            model_name='babycare',
            name='endorsement',
        ),
        migrations.RemoveField(
            model_name='babycare',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='babycare',
            name='nutrition',
        ),
        migrations.DeleteModel(
            name='Details',
        ),
        migrations.AddField(
            model_name='babycaredetails',
            name='babycare',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.BabyCare'),
        ),
        migrations.AddField(
            model_name='babycaredetails',
            name='nutrition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deltago.Nutrition'),
        ),
    ]
