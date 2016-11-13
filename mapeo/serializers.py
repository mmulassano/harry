from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from mapeo.models import Post, Farm, TypeCrop, Parcel, Activity

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'mobile_id')

class TypeCropSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = TypeCrop
       fields = ('id','name')


class FarmSerializer(serializers.HyperlinkedModelSerializer):
   # id = serializers.IntegerField(read_only=True)
   #id_user = serializers.IntegerField(required=True)
   # nombre = serializers.CharField(required=True)
   # mobile_id = serializers.IntegerField(required=True)

   class Meta:
       model = Farm
       fields = ('user_id','name','active','movil_id')


class ParcelSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Parcel
       fields = ('movil_id','farm_id','name','surface','user_id','active','center_lat','center_long')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Activity
       fields = ('movil_id','parcel_id','type_crop_id','campaign','user_id','date','active')



