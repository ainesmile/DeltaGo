# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-29 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babycare',
            name='category',
            field=models.CharField(choices=[('B', 'BabyCare'), ('F', 'Food'), ('P', 'Supplement'), ('U', 'Beauty'), ('S', 'Special')], default='B', max_length=2),
        ),
    ]
