from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
    user_id = models.IntegerField()
    type_object = models.CharField(max_length=100)  #parcel,farm,user
    object_id = models.BigIntegerField()
    order = models.IntegerField()
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)

