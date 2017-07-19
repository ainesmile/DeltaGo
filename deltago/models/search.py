from __future__ import unicode_literals

from django.db import models
from deltago.models import Commodity

class Search(models.Model):
    name = models.CharField(max_length = 128)
    commodity = models.ForeignKey('Commodity', on_delete=models.CASCADE)
    def __str__(self):
        return self.name