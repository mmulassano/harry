from django.http import HttpResponse
from django.shortcuts import render

#...........
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from models import Post, Farm, TypeCrop, Parcel, Activity
from serializers import PostSerializer, FarmSerializer, TypeCropSerializer, ParcelSerializer, ActivitySerializer

from django.core import serializers
from django.http import HttpResponse
from django.db import transaction, IntegrityError

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
import datetime

#...........


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #authentication_classes = (TokenAuthentication)
    #permission_classes = (IsAuthenticated,)


    def get_response_data(self, user):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            posts = Post.objects.filter(mobile_id=request.POST['mobile_id'])
            registro = Post.objects.filter(mobile_id=request.POST['mobile_id']).count()
            if (registro == 0):
                # CREO
                serializer = PostSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.id_user = request.user.id
                    print request.user.id
                    serializer.save(id_user=request.user.id)
                    #return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                # ACTUALIZO
                posts = Post.objects.filter(mobile_id=request.POST['mobile_id'])
                for objectPost in posts:
                    serializer = PostSerializer(objectPost, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        #return Response(serializer.data)
                        return Response(status=status.HTTP_201_CREATED)
                    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(status=status.HTTP_400_BAD_REQUEST)



#Campos - Farm este metodo seria para web que no trabaja con id_movil
"""
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    #queryset = self.get_queryset()
    serializer_class = FarmSerializer
    #authentication_classes = (TokenAuthentication)
    #permission_classes = ()

    def create(self, request):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    for registro in request.data:
                        registro['id_user'] = request.user.id
                        movil_id = registro['movil_id']
                        #print registro
                        farm = Farm.objects.filter(movil_id=movil_id)
                        existen = Farm.objects.filter(movil_id=movil_id).count()
                        if (existen == 0):
                            serializer = FarmSerializer(data=registro)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise AttributeError
                        else:
                            # ACTUALIZO
                            farm = Farm.objects.filter(movil_id=movil_id)
                            for objectFarm in farm:
                                serializer = FarmSerializer(objectFarm, data=registro)
                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    raise AttributeError
            except (AttributeError, ObjectDoesNotExist):
                pass
                return Response({"error": ("NO GUARDA NADA")},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": ("GUARDA TODO")},
                            status=status.HTTP_200_OK)



"""


##########FARM
##################################
#Agrega y modifica campo por id_movil
@api_view(['GET', 'POST'])
def farm(request):
    if request.method == 'POST':
          try:
              with transaction.atomic():
                  for registro in request.data:
                     registro['user_id'] = request.user.id
                     registro['activo'] = True
                     movil_id = registro['movil_id']
                     farm = Farm.objects.filter(movil_id=movil_id)
                     existen = Farm.objects.filter(movil_id=movil_id).count()
                     if (existen == 0):
                         serializer = FarmSerializer(data=registro)
                         if serializer.is_valid():
                             serializer.save()
                         else:
                             raise AttributeError
                     else:
                         # ACTUALIZO
                         farm = Farm.objects.filter(movil_id=movil_id)
                         for objectFarm in farm:
                              serializer = FarmSerializer(objectFarm, data=registro)
                              if serializer.is_valid():
                                   serializer.save()
                              else:
                                   raise AttributeError

              return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
          except (AttributeError, ObjectDoesNotExist):
              pass
              return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
          farms = Farm.objects.filter(user_id=request.user.id,active=True)
          serializer = FarmSerializer(farms, many=True)
          return JSONResponse(serializer.data)

# Elimina campo por id_movil
@api_view(['DELETE'])
def farmDelete(request):
    if request.method == 'DELETE':
        try:
            with transaction.atomic():
                for registro in request.data:
                    movil_id = registro['movil_id']
                    #ACTUALIZO
                    farm = Farm.objects.filter(movil_id=movil_id,user_id=request.user.id)
                    for objectFarm in farm:
                        registro['user_id'] = objectFarm.user_id
                        registro['name'] = objectFarm.name
                        registro['active'] = False
                        serializer = FarmSerializer(objectFarm, data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
            return Response({"success": ("ELIMINA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO ELIMINA NADA")}, status=status.HTTP_400_BAD_REQUEST)


#############################  PARCEL
######################################
# Agrega y modifica parcela por id_movil
@api_view(['POST', 'GET'])
def parcel(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for registro in request.data:
                    registro['user_id'] = request.user.id
                    movil_id = registro['movil_id']
                    parcel = Parcel.objects.filter(movil_id=movil_id)
                    existen = Parcel.objects.filter(movil_id=movil_id).count()
                    if (existen == 0):
                        serializer = ParcelSerializer(data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
                    else:
                        # ACTUALIZO
                        parcel = Parcel.objects.filter(movil_id=movil_id)
                        for objectParcel in parcel:
                            serializer = ParcelSerializer(objectParcel, data=registro)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise AttributeError
            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        parcels = Parcel.objects.filter(user_id=request.user.id,active=True)
        serializer = ParcelSerializer(parcels, many=True)
        return JSONResponse(serializer.data)



#consulta lotes por campo
@api_view(['GET'])
def parcelFarm(request, farm_id):
    if request.method == 'GET':
         parcels = Parcel.objects.filter(user_id=request.user.id, farm_id=farm_id)
         serializer = ParcelSerializer(parcels, many=True)
         return JSONResponse(serializer.data)


#Elimina parcela por id_movil recibe una lista de movil_id
@api_view(['DELETE'])
def parcelDelete(request):
    if request.method == 'DELETE':
        try:
            with transaction.atomic():
                for registro in request.data:
                    movil_id = registro['movil_id']
                    #ACTUALIZO
                    parcel = Parcel.objects.filter(movil_id=movil_id,user_id=request.user.id)
                    for objectParcel in parcel:
                        registro['user_id'] = objectParcel.user_id
                        registro['farm_id'] = objectParcel.farm_id
                        registro['surface'] = objectParcel.surface
                        registro['center_lat'] = objectParcel.center_lat
                        registro['center_long'] = objectParcel.center_long
                        registro['name'] = objectParcel.name
                        registro['active'] = False
                        serializer = ParcelSerializer(objectParcel, data=registro)
                        if serializer.is_valid():
                            serializer.save()
                            """
                            #actualizo actividades con ese parcel_id
                            parcel_id = registro['movil_id']
                            # ACTUALIZO Actividades

                            activity = Activity.objects.filter(parcel_id=parcel_id, user_id=request.user.id)
                            for objectActivity in activity:
                                registro['movil_id'] = objectActivity.user_id
                                registro['user_id'] = objectActivity.user_id
                                registro['parcel_id'] = objectActivity.parcel_id
                                registro['type_crop_id'] = objectActivity.type_crop_id
                                registro['campaign'] = objectActivity.campaign
                                registro['date'] = objectActivity.date
                                registro['active'] = False
                                serializer2 = ActivitySerializer(objectActivity, data=registro)
                                if serializer2.is_valid():
                                    serializer2.save()
                                else:
                                    raise AttributeError
                            """
                        else:
                            raise AttributeError
            return Response({"success": ("ELIMINA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO ELIMINA NADA")}, status=status.HTTP_400_BAD_REQUEST)


##### ACTIVITY
##################################
# Agrega y modifica actividades de lote
@api_view(['POST', 'GET'])
def activity(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for registro in request.data:
                    registro['user_id'] = request.user.id
                    movil_id = registro['movil_id']
                    activity = Activity.objects.filter(movil_id=movil_id)
                    existen = Activity.objects.filter(movil_id=movil_id).count()
                    if (existen == 0):
                        serializer = ActivitySerializer(data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
                    else:
                        # ACTUALIZO
                        activity = Activity.objects.filter(movil_id=movil_id)
                        for objectActivity in activity:
                            serializer = ActivitySerializer(objectActivity, data=registro)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                raise AttributeError
            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        activitys = Activity.objects.filter(user_id=request.user.id,active=True)
        serializer = ActivitySerializer(activitys, many=True)
        return JSONResponse(serializer.data)

# Elimina parcela por id_movil recibe una lista de movil_id
@api_view(['DELETE'])
def activityDelete(request):
    if request.method == 'DELETE':
        try:
            with transaction.atomic():
                for registro in request.data:
                    movil_id = registro['movil_id']
                    # ACTUALIZO
                    activity = Activity.objects.filter(movil_id=movil_id, user_id=request.user.id)
                    for objectActivity in activity:
                        registro['user_id'] = objectActivity.user_id
                        registro['parcel_id'] = objectActivity.parcel_id
                        registro['type_crop_id'] = objectActivity.type_crop_id
                        registro['campaign'] = objectActivity.campaign
                        registro['date'] = objectActivity.date
                        registro['active'] = False
                        serializer = ActivitySerializer(objectActivity, data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
            return Response({"success": ("ELIMINA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO ELIMINA NADA")}, status=status.HTTP_400_BAD_REQUEST)


# if request.method == 'POST':
# for diccionario in request.data:
# diccionario['id_user']=request.user.id
# return JSONResponse(diccionario)



#Tipos de cultivo
class TypeCropViewSet(viewsets.ModelViewSet):
    queryset = TypeCrop.objects.all()
    serializer_class = TypeCropSerializer

from django.http import JsonResponse

#Listado de campanias
@api_view(['GET'])
def list_campaign(request):
    if request.method == 'GET':
        momento_actual = datetime.datetime.now()
        anio_actual = momento_actual.year
        list_cam = []
        periodo = str(anio_actual + 1) + "-" + str(anio_actual + 2)
        dato = {"campaign": periodo}
        list_cam.append(dato)
        periodo =  str(anio_actual) + "-" + str(anio_actual + 1)
        dato = {"campaign": periodo}
        list_cam.append(dato)
        anio = anio_actual
        for indice in range(1,2):
            periodo =  str(anio_actual - 1) + "-" + str(anio_actual)
            dato = {"campaign":  periodo }
            list_cam.append(dato)
            anio_actual = anio_actual - 1
        return JSONResponse(list_cam)
        #return JSONResponse(list_cam) {"key": "value"}



