from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Commodity(models.Model):
    name = models.CharField(max_length = 128)
    volume_size = models.CharField(max_length = 128,)
    price = models.CharField(max_length = 128,)
    was_price = models.CharField(max_length = 128, null = True, blank = True)
    special_price = models.CharField(max_length = 128, null = True, blank = True)
    category = models.CharField(max_length = 20)
    sub_category = models.CharField(max_length = 20)
    stockcode = models.CharField(max_length = 20, null = True, blank = True)
    online_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name

class Details(models.Model):
    commodity = models.ForeignKey('Commodity', on_delete=models.CASCADE)
    pic_url = models.URLField(blank = True, null = True)
    description = models.TextField(null = True, blank = True)
    nutrition = models.TextField(max_length = 128, null = True, blank = True)
    ingredient = models.CharField(max_length = 128, null = True, blank = True)
    claim = models.CharField(max_length = 128, null = True, blank = True)
    endorsement = models.CharField(max_length = 128, null = True, blank = True)