from django.db import models

class Cart(models.Model):
    commodity_id = models.CharField(max_length = 128, unique = True)
    model_name = models.CharField(max_length = 128)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.stockcode