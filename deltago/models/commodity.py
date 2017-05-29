from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from deltago.models.nutrition import Nutrition

class Commodity(models.Model):
    BABYCARE = 'B'
    FOOD = 'F'
    SUPPLEMENT = 'P'
    BEAUTY = 'U'
    SPECIAL = 'S'

    CATEGORY_CHOICES = (
        (BABYCARE, 'BabyCare'),
        (FOOD, 'Food'),
        (SUPPLEMENT, 'Supplement'),
        (BEAUTY, 'Beauty'),
        (SPECIAL, 'Special'),
    )

    name = models.CharField(
        max_length = 128,
        unique=True)
    brand = models.CharField(max_length=128)
    origin = models.CharField(
        max_length = 128,
        null = True,
        blank = True)
    price = models.IntegerField()
    discount = models.IntegerField(
        blank = True,
        null = True)
    pic_url = models.URLField(
        blank = True,
        null = True)
    category = models.CharField(
        max_length = 2,
        choices = CATEGORY_CHOICES,
        default = BABYCARE,)
    description = models.TextField(
        default = name)
    online_date = models.DateTimeField(
        default = timezone.now)

    class Meta:
        abstract = True
        ordering = ['brand', 'name']

    def __str__(self):
        return self.name



class BabyCare(Commodity):
    FOOD = 'F'
    FOOD_4M = 'F4'
    FOOD_6M = 'F6'
    FOOD_9M = 'F9'
    FOOD_12M = 'F12'
    MEDICINAL = 'M'
    SUB_CATEGORY = (
        (FOOD, 'Other Baby Foods'),
        (FOOD_4M, 'Baby Food From 4 Mths'),
        (FOOD_6M, 'Baby Food From 6 Mths'),
        (FOOD_9M, 'Baby Food From 9 Mths'),
        (FOOD_12M, 'Baby Food From 12 Mths'),
        (MEDICINAL, 'Medicinal Needs'),
    )

    weight = models.CharField(
        max_length = 128,)
    cup_price = models.IntegerField()
    ingredient = models.TextField()
    claim = models.TextField()
    endorsement = models.TextField()
    nutrition = models.ForeignKey(Nutrition)

    sub_category = models.CharField(
        max_length = 3,
        choices = SUB_CATEGORY,
        default = FOOD)