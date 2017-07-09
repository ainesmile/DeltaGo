from __future__ import unicode_literals

from django.db import models

class Search(models.Model):
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

    name = models.CharField(max_length = 128)
    stockcode = models.CharField(max_length = 128, unique = True)
    model_name = models.CharField(max_length = 128)
    def __str__(self):
        return self.name