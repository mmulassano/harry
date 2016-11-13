from django.contrib.auth.models  import User, Group
from models import TypeUser, Profile
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
        model = Group
        fields = ('url', 'name')


class TypeUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeUser
        fields = ('codigo', 'nombre')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
        model = Profile
        fields = ('user_id','name', 'photo')



    #def validate(self, data):
     #   if data['codigo'] == 1:
      #      raise serializers.ValidationError(("El codigo se repite"))
