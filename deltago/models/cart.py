from django.db import models

class Cart(models.Model):
    commodity_id = models.IntegerField(unique = True)
    model_name = models.CharField(max_length = 128)
    quantity = models.IntegerField(default=0)