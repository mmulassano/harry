from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import viewsets, request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from models import Location
from serializers import LocationSerializer

from django.http import HttpResponse
from django.db import transaction, IntegrityError

from django.core.exceptions import ObjectDoesNotExist
import datetime



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#Agrega y modifica campo por id_movil
@api_view(['GET', 'POST'])
def location(request):
    if request.method == 'POST':
          try:
              with transaction.atomic():
                  for registro in request.data:
                     registro['user_id'] = request.user.id
                     #type_object = registro['type_object']
                     object_id = registro['object_id']
                     existen = Location.objects.filter(object_id=object_id).count()

                  if (existen == 0):
                      #Si no existe guardo todos los registros
                      for registro in request.data:
                         serializer = LocationSerializer(data=registro)
                         if serializer.is_valid():
                             serializer.save()
                         else:
                             raise AttributeError

                  else:
                         # Elimino todos los pun tos de ese objeto
                         location = Location.objects.filter(object_id=object_id)
                         for objectLocation in location:
                             objectLocation.delete()

                         # guardo todos los registros
                         for registro in request.data:
                            serializer = LocationSerializer(data=registro)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise AttributeError


              return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
          except (AttributeError, ObjectDoesNotExist):
              pass
              return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
          locations = Location.objects.filter(user_id=request.user.id)
          serializer = LocationSerializer(locations, many=True)
          return JSONResponse(serializer.data)
