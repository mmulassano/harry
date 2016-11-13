from __future__ import unicode_literals

from django.db import models

#Tipos de Amenazas - type threat
class TypeThreat(models.Model):
   code =  models.IntegerField(unique=True)
   name = models.CharField(max_length=100,unique=True)

#Amenazas - threat
class Threat(models.Model):
   code =  models.IntegerField()
   typeThreat_id = models.IntegerField()
   name = models.CharField(max_length=100,unique=True)
   scientific_name = models.CharField(max_length=100,unique=True)
   description = models.CharField(max_length=300)
   wikipedia_link =  models.CharField(max_length=400)
   active = models.BooleanField(default=True)

#Detalle Amenaza - threat detail
class ThreatDetail(models.Model):
   typeCrop_id = models.IntegerField()
   threat_id = models.IntegerField()
   rango_alcance = models.IntegerField()
   expiracion = models.CharField(max_length=100)

class Detection(models.Model):
   user_id = models.IntegerField()
   threatDetail_id = models.BigIntegerField()
   activity_id = models.BigIntegerField()
   #location_id = models.CharField(max_length=100)
   #source = models.CharField(max_length=100)
   #source_score = models.CharField(max_length=100)
   date = models.CharField(max_length=100)
   damage_level = models.IntegerField()
   movil_id = models.BigIntegerField()
   location_lat = models.CharField(max_length=100)
   location_long = models.CharField(max_length=100)   

class Seen(models.Model):
   user_id = models.IntegerField()
   object_id = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   date_time = models.IntegerField()

class Note(models.Model):
   object_id = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   content = models.CharField(max_length=300)
   user_id = models.IntegerField()

class Picture(models.Model):
   object_id = models.BigIntegerField()
   object_type = models.CharField(max_length=100)
   image = models.ImageField(upload_to='img',null=True)

