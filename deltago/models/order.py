from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from deltago.models import Cart

class Order(models.Model):
    UNPAID = 'U'
    ARCHIVED = 'A'
    PROCESSING = 'P'
    CANCELING = 'C'
    FINISHED = 'F'
    STATES = (
        (UNPAID, 'Unpaid'),
        (ARCHIVED, 'Archived'),
        (PROCESSING, 'Processing'),
        (CANCELING, 'Canceling'),
        (FINISHED, 'Finished')
    )
    
    cart = models.ForeignKey(Cart)
    state = models.CharField(max_length=2, choices=STATES, default=UNPAID)
    
    payment_method = models.CharField(
        max_length=128,
        default = None,
        null=True,
        blank=True)
    ship_address = models.CharField(
        max_length=200,
        default = None,
        null=True,
        blank=True)
    
    exchange_rate = models.IntegerField(
        default=500,
        null=True,
        blank=True,)
    subtotal = models.IntegerField()
    total = models.IntegerField()
    
    user = models.ForeignKey(User)
    

    # unpaind_time is order's created_time
    unpaind_time = models.DateTimeField(default=timezone.now)
    archived_time = models.DateTimeField(null = True, blank = True)
    processing_time = models.DateTimeField(null = True, blank = True)
    canceling_time = models.DateTimeField(null = True, blank = True)
    finished_time = models.DateTimeField(null = True, blank = True)

    class Meta:
        ordering = ['-unpaind_time']

class Ship(models.Model):
    SEND = 'S'
    PROCESSING = 'P'
    DELIVERED = 'D'

    STATES = (
        (SEND, 'Send'),
        (PROCESSING, 'Processing'),
        (DELIVERED, 'Delivered')
    )

    order = models.ForeignKey('Order')
    number = models.CharField(max_length=128)
    express = models.CharField(max_length=128)
    linker = models.URLField()
    fee = models.IntegerField()
    address = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    signer = models.CharField(max_length=128)

    send_time = models.DateTimeField(default=timezone.now)
    processing_time = models.DateTimeField(default=timezone.now)
    delivered_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.number


class Payment(models.Model):
    order = models.ForeignKey('Order')
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=200)
    method = models.CharField(max_length=128)
    ship_fee = models.IntegerField()
    subtotal = models.IntegerField()
    currency_unit = models.CharField(max_length=128)
    exchange_rate = models.IntegerField()
    created_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.order