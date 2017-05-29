from __future__ import unicode_literals

from django.db import models

class Nutrition(models.Model):
    
    serving_pack = models.IntegerField()
    serving_size = models.CharField(
        max_length = 128,)

    enegry_per_serving = models.CharField(
        max_length = 128,)
    enegry_per_100g = models.CharField(
        max_length = 128,)

    enegry_per_serving = models.CharField(
        max_length = 128,)
    enegry_per_100g = models.CharField(
        max_length = 128,)

    protein_per_serving = models.CharField(
        max_length = 128,)
    protein_per_100g = models.CharField(
        max_length = 128,)

    fat_per_serving = models.CharField(
        max_length = 128,)
    fat_per_100g = models.CharField(
        max_length = 128,)

    carbohydrate_per_serving = models.CharField(
        max_length = 128,)
    carbohydrate_per_100g = models.CharField(
        max_length = 128,)

    sugars_per_serving = models.CharField(
        max_length = 128,)
    sugars_per_100g = models.CharField(
        max_length = 128,)

    sodium_per_serving = models.CharField(
        max_length = 128,)
    sodium_per_100g = models.CharField(
        max_length = 128,)
