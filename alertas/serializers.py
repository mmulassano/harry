from rest_framework import serializers
from alertas.models import TypeThreat, Threat, ThreatDetail,Seen,Detection,Picture,Note

class TypeThreatSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = TypeThreat
       fields = ('id','name','code')


class ThreatSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Threat
       fields = ('code','name','typeThreat_id','scientific_name','description','wikipedia_link','active')



class ThreatDetailSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = ThreatDetail
       fields = ('typeCrop_id','threat_id','rango_alcance','expiracion')


class DetectionSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Detection
       fields = ('user_id','threatDetail_id','date','damage_level','movil_id','activity_id','location_lat','location_long')


class SeenSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Seen
       fields = ('user_id','object_id','object_type','date_time')


class NoteSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Note
       fields = ('object_id','object_type','content','user_id')


class PictureSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Picture
       fields = ('object_id','object_type','image')

