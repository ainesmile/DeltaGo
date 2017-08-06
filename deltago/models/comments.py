from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Comment(models.Model):
    author = models.ForeignKey(User)
    nickname = models.CharField(max_length=20, null=True, blank=True, default=None)
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    useful_number = models.IntegerField(default=0)
    unuseful_number = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=True)

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['useful_number']

# only superuser can reply
class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    author = models.ForeignKey(User)
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.content

