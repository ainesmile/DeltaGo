# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-16 09:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deltago', '0015_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodities', models.CharField(max_length=500)),
                ('prices', models.CharField(max_length=500)),
                ('quantities', models.CharField(max_length=250)),
                ('state', models.CharField(choices=[('U', 'Unpaid'), ('A', 'Archived'), ('P', 'Processing'), ('C', 'Canceling'), ('F', 'Finished')], default='U', max_length=2)),
                ('payment_method', models.CharField(max_length=128)),
                ('ship_address', models.CharField(max_length=200)),
                ('exchange_rate', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('total', models.IntegerField()),
                ('unpaind_time', models.DateField(default=django.utils.timezone.now)),
                ('archived_time', models.DateField(blank=True, null=True)),
                ('processing_time', models.DateField(blank=True, null=True)),
                ('canceling_time', models.DateField(blank=True, null=True)),
                ('finished_time', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-unpaind_time'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('number', models.CharField(max_length=200)),
                ('method', models.CharField(max_length=128)),
                ('ship_fee', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('currency_unit', models.CharField(max_length=128)),
                ('exchange_rate', models.IntegerField()),
                ('created_time', models.DateField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128)),
                ('express', models.CharField(max_length=128)),
                ('linker', models.URLField()),
                ('fee', models.IntegerField()),
                ('address', models.CharField(max_length=128)),
                ('receiver', models.CharField(max_length=128)),
                ('signer', models.CharField(max_length=128)),
                ('send_time', models.DateField(default=django.utils.timezone.now)),
                ('processing_time', models.DateField(default=django.utils.timezone.now)),
                ('delivered_time', models.DateField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.Order')),
            ],
        ),
    ]