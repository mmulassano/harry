from rest_framework import serializers
from pushes.models import Device

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('user_id', 'active','key_firebase')