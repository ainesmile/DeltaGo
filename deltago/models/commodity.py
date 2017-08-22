from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Commodity(models.Model):
    name = models.CharField(max_length = 128)
    price = models.IntegerField(default = 0, null = True, blank = True)
    special_price = models.IntegerField(default = 0, null = True, blank = True)
    volume_size = models.CharField(max_length = 128, null = True, blank = True)
    category = models.CharField(max_length = 20)
    online_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name

class Details(models.Model):
    commodity = models.ForeignKey('Commodity', on_delete=models.CASCADE)
    ingredient = models.CharField(max_length = 128, null = True, blank = True)
    serving_size = models.CharField(max_length = 16, null = True, blank = True)
    servings = models.IntegerField(null = True, blank = True)
    nutritions = models.TextField(max_length = 512, null = True, blank = True)
    claims = models.CharField(max_length = 128, null = True, blank = True, default=None)
    health_star_rating = models.IntegerField(null = True, blank = True, default=None)

    weight = models.CharField(max_length = 16, null = True, blank = True, default=None)
    made_in = models.CharField(max_length = 128, null = True, blank = True, default=None)
    pic_url = models.URLField(blank = True, null = True, default=None)
    description = models.TextField(null = True, blank = True, default=None)
    endorsement = models.CharField(max_length = 128, null = True, blank = True, default=None)

