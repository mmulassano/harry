from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Device(models.Model):
    #name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    user_id = models.IntegerField()
    #device_id = models.IntegerField()
    key_firebase = models.CharField(max_length=500)
    #date_create = models.CharField(max_length=100)
