from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
from django.db import transaction

from models import Device
from serializers import DeviceSerializer
from django.core.exceptions import ObjectDoesNotExist

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



"""
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            for registro in request.data:
                registro['user_id'] = request.user.id
                registro['activo'] = True
                serializer = DeviceSerializer(data=registro)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

"""


#grega key_firebase por dispositivos
@api_view(['GET', 'POST'])
def device(request):
    if request.method == 'POST':
          try:
              with transaction.atomic():
                  print request.data["key_firebase"]
                  request.data['user_id'] = request.user.id
                  request.data['active'] = True
                  existen = Device.objects.filter(key_firebase=request.data['key_firebase']).count()
                  #('user_id', 'active', 'key_firebase')
                  if(existen == 0):
                    serializer = DeviceSerializer(data=request.data)
                    if serializer.is_valid():
                         serializer.save()
                    else:
                         raise AttributeError

              return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
          except (AttributeError, ObjectDoesNotExist):
              pass
              return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
          devices = Device.objects.filter(active=True)
          serializer = DeviceSerializer(devices, many=True)
          return JSONResponse(serializer.data)


from pyfcm import FCMNotification

def push_notifications_view(key_firebase,title,body,data_message):

    #push_service = FCMNotification(api_key="AIzaSyA8QwUuPK3NGlUTJRXhqZpL1exe-_KQ25E")
    push_service = FCMNotification(api_key="AIzaSyAcsKhb9kYVJ0WzDlVVQ0HK7v-QfvaR1Cs")
    registration_id = key_firebase
    #registration_id = "cHm7onyVfg8:APA91bE_yIhRAlVw9Gsua1zPyTWPQ8MQ5NAmSWWLar7Kr0x9-T8Vl0teBmsFhnseaPcu9gddZVKNdMnA97DWKD7-n_7nSdkIpNqdSGfHeV3ELAMH0W2z6tecJz3mjj7Hw-J6e7E-aAbe"
    message_title = title
    message_body = body
    data_message = data_message
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,message_body=message_body,data_message=data_message)

    return result

    #Device = get_device_model()
    #Device.objects.all().send_message({'message':'Prueba push desde back'})


   #FCMMessage().send({'message':'Prueba push desde back'}, to='ar.com.nexosoluciones.android.harryapp')
   #msj = "mensaje enviado a los dispositivos Android"
   #return JSONResponse(msj)
