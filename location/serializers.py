from rest_framework import serializers
from location.models import Location

class LocationSerializer(serializers.ModelSerializer):

   class Meta:
       model = Location
       fields = ('id','user_id','type_object','object_id','order','lat','long')
