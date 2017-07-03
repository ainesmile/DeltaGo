from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Commodity(models.Model):
    BABYCARE = 'B'
    FOOD = 'F'
    SUPPLEMENT = 'P'
    BEAUTY = 'U'
    SPECIAL = 'S'

    CATEGORY = (
        (BABYCARE, 'BabyCare'),
        (FOOD, 'Food'),
        (SUPPLEMENT, 'Supplement'),
        (BEAUTY, 'Beauty'),
        (SPECIAL, 'Special'),
    )
    stockcode = models.CharField(max_length = 128, unique = True, null = True, blank = True)
    name = models.CharField(max_length = 128)
    volume_size = models.CharField(max_length = 128,)
    price = models.CharField(max_length = 128,)
    was_price = models.CharField(max_length = 128, null = True, blank = True)
    special_price = models.CharField(max_length = 128, null = True, blank = True)
    category = models.CharField(max_length = 2, choices = CATEGORY, default = BABYCARE,)
    
    online_date = models.DateTimeField(default = timezone.now)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

class Details(models.Model):
    stockcode = models.CharField(max_length = 128, unique = True, null = True, blank = True)
    name = models.CharField(max_length = 128, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    pic_url = models.URLField(blank = True, null = True)
    class Meta:
        abstract = True

class BabyCareDetails(Details):
    nutrition = models.TextField(max_length = 128, null = True, blank = True)
    ingredient = models.CharField(max_length = 128, null = True, blank = True)
    claim = models.CharField(max_length = 128, null = True, blank = True)
    endorsement = models.CharField(max_length = 128, null = True, blank = True)

class BabyCare(Commodity):
    FOOD = 'F'
    FOOD_4M = 'F4'
    FOOD_6M = 'F6'
    FOOD_9M = 'F9'
    FOOD_12M = 'F12'
    MEDICINAL = 'M'
    TOILETRY = 'T'
    NAPPY = 'N'
    SUB_CATEGORY = (
        (FOOD, 'Other Baby Foods'),
        (FOOD_4M, 'Baby Food From 4 Mths'),
        (FOOD_6M, 'Baby Food From 6 Mths'),
        (FOOD_9M, 'Baby Food From 9 Mths'),
        (FOOD_12M, 'Baby Food From 12 Mths'),
        (MEDICINAL, 'Medicinal Needs'),
        (TOILETRY, 'toiletries'),
        (NAPPY, 'nappies and liners'),
    )

    sub_category = models.CharField(
        max_length = 3,
        choices = SUB_CATEGORY,
        default = FOOD)
    details = models.ForeignKey(BabyCareDetails, null = True, blank = True)