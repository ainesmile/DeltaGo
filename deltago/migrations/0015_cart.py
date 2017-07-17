# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-11 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deltago', '0014_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockcode', models.CharField(max_length=128, unique=True)),
                ('model_name', models.CharField(max_length=128)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
    ]