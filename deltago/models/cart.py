from django.db import models
from deltago.models import Commodity

class Cart(models.Model):
    commodity = models.ForeignKey('Commodity', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)