# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 08:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('volume_size', models.CharField(max_length=128)),
                ('price', models.CharField(blank=True, max_length=128, null=True)),
                ('was_price', models.CharField(blank=True, max_length=128, null=True)),
                ('special_price', models.CharField(blank=True, max_length=128, null=True)),
                ('category', models.CharField(max_length=20)),
                ('sub_category', models.CharField(max_length=20)),
                ('stockcode', models.CharField(max_length=20, unique=True)),
                ('online_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('nutrition', models.TextField(blank=True, max_length=128, null=True)),
                ('ingredient', models.CharField(blank=True, max_length=128, null=True)),
                ('claim', models.CharField(blank=True, max_length=128, null=True)),
                ('endorsement', models.CharField(blank=True, max_length=128, null=True)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.Commodity')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodities', models.CharField(max_length=500)),
                ('prices', models.CharField(max_length=500)),
                ('quantities', models.CharField(max_length=250)),
                ('state', models.CharField(choices=[('U', 'Unpaid'), ('A', 'Archived'), ('P', 'Processing'), ('C', 'Canceling'), ('F', 'Finished')], default='U', max_length=2)),
                ('payment_method', models.CharField(blank=True, max_length=128, null=True)),
                ('ship_address', models.CharField(blank=True, max_length=200, null=True)),
                ('exchange_rate', models.IntegerField(blank=True, null=True)),
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
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.Commodity')),
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
        migrations.AddField(
            model_name='cart',
            name='commodity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deltago.Commodity'),
        ),
    ]
