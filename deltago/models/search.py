from __future__ import unicode_literals

from django.db import models

class Search(models.Model):
    name = models.CharField(max_length = 128)
    commodity_id = models.IntegerField(unique = True, default=1)
    model_name = models.CharField(max_length = 128)
    def __str__(self):
        return self.name