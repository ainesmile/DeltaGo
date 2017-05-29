from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Commodity(models.Model):
    BABY = 'B'
    FOOD = 'F'
    HEALTH = 'H'
    BEAUTY = 'Y'
    SPECIAL = 'S'
    CATEGORY = (
        (BABY, 'Baby')
        (FOOD, 'Food'),
        (HEALTH, 'Health'),
        (BEAUTY, 'Beauty'),
        (SPECIAL, 'Special'),
    )

    name = models.CharField(
        max_length=128,
        unique=True)
    brand = models.CharField(max_length=128)
    origin = models.CharField(
        max_length=128,
        null=True,
        blank=True)
    price = models.IntegerField()
    discount = models.IntegerField(
        blank=True,
        null=True)
    pic_url = models.URLField(
        blank=True,
        null=True)
    category = models.CharField(
        choices=CATEGORY
        default=CATEGORY.BABY)
    description = models.TextField(
        default=name)
    online_date = models.DateTimeField(
        default = timezone.now)

    class Meta:
        abstract = True
        ordering = ['brand', 'name']

    def __str__(self):
        return self.name