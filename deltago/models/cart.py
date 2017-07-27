from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from deltago.models import Commodity

class Cart(models.Model):
    commodities = models.ManyToManyField(Commodity, through='Cartship')
    user = models.ForeignKey(User)
    is_archived = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

class Cartship(models.Model):
    commodity = models.ForeignKey(Commodity)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField(default=0)
    is_choosed = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)