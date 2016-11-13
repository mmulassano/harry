from django.shortcuts import render
from models import ThreatDetail,Threat,TypeThreat,Detection,Seen,Note,Picture
from mapeo.models import Activity, Parcel,TypeCrop
from pushes.models import Device
from pushes.views import push_notifications_view
from usuario.models import Profile
from rest_framework import viewsets
from serializers import TypeThreatSerializer,ThreatDetailSerializer,  ThreatSerializer, DetectionSerializer,NoteSerializer,PictureSerializer,SeenSerializer

from rest_framework.decorators import api_view
from rest_framework import viewsets, request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from pyfcm import FCMNotification

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.core.exceptions import ObjectDoesNotExist
import datetime
from harry import settings
#...........
from django.contrib.auth import get_user_model
UserModel = get_user_model()

import json



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class TypeThreatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TypeThreat.objects.all().order_by()
    serializer_class = TypeThreatSerializer



class ThreatViewSet(viewsets.ModelViewSet):
    queryset = Threat.objects.all().order_by()
    serializer_class = ThreatSerializer

class NoteViewSet(viewsets.ModelViewSet):
        queryset = Note.objects.all().order_by()
        serializer_class = NoteSerializer


##########AMENAZAS
##################################
#consulta de las amenazas,
@api_view(['GET'])
def threat(request):
    if request.method == 'GET':
       #threats = Threat.objects.filter()
       #serializer = ThreatSerializer(threats, many=True)
       threatDetails = ThreatDetail.objects.filter()
       list_threat = []

       for objectThreatDetail in threatDetails:
           #serializer = ThreatSerializer(objectThreat)
            id_threat=objectThreatDetail.threat_id
            threats = Threat.objects.filter(id=id_threat)
            for objectThreat in threats:
                name = objectThreat.name
                scientific_name= objectThreat.scientific_name
                description = objectThreat.description
                wikipedia_link = objectThreat.wikipedia_link

            datatime = ""
            distance_min = 0
            valorization = 0
            sum_detection=0
            sum_seen = 0
            image_url='sin imagen'
            detection = Detection.objects.filter(threatDetail_id=objectThreatDetail.id)
            for objectDetection in detection:
                sum_detection = sum_detection +1
                datatime =  objectDetection.date
                distance_min = 2.5
                valorization = 3

                picture = Picture.objects.filter(object_id=objectDetection.movil_id)
                for objectPicture in picture:
                    image_url = "picture/img/images_X3QUPKG.jpg"
		    #objectPicture.image

                seens = Seen.objects.filter(object_id=id_threat, object_type="threat")
                for objectSeen in seens:
                    sum_seen = sum_seen + 1


            dato = {
                    "threat_id":id_threat,
                    "name": name,
                    "scientific_name": scientific_name,
                    "description": description,
                    "wikipedia_link": wikipedia_link,
                    "typeThreat_id":objectThreat.typeThreat_id,
                    "crop_id": objectThreatDetail.typeCrop_id,
                    "detection_sum": sum_detection,
                    "seen_sum": sum_seen,
                    "image": image_url,
                    "datetime_last": datatime,
                    "distance_min": distance_min,
                    "valorization": valorization         #0 - 4
                }
            list_threat.append(dato)
       return JSONResponse(list_threat)


#Nueva amenaza

#Agrega AMENAZA
@api_view(['POST'])
def threatNew(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():

                datos_threat= {}
                datos_threatDetail = {}
                datos_detection = {}
                datos_note = {}

                threat_id = 0
                threat = Threat.objects.filter(name=request.POST['name'],scientific_name=request.POST['scientific_name'])
                if (threat.count() > 0):
                    for objectThreat in threat:
                        threat_id = objectThreat.id
                else:
                    threat = Threat.objects.filter(scientific_name=request.POST['scientific_name'])
                    if(threat.count() > 0):
                        for objectThreat in threat:
                            threat_id = objectThreat.id
                    else:
                        threat = Threat.objects.filter(name=request.POST['name'])
                        if (threat.count() > 0):
                            for objectThreat in threat:
                                threat_id = objectThreat.id

                if(threat_id != 0):
                    #ver si existe el detalle
                    threatDetail = ThreatDetail.objects.filter(threat_id=threat_id,typeCrop_id=request.POST['crop_id'])
                    #si exite, registro deteccion
                    if (threatDetail.count() > 0):
                        for objectThreatDetail in threatDetail:
                            threatDetail_id = objectThreatDetail.id
                            print threatDetail_id
                            request.POST['threat_id'] = threatDetail_id
                            print "deteccion"

                            #inicio deteccion
                            detection(request.data)
                            ##Fin deteccion


                    else:
                        #agrego detalle amenaza, aun no cargo la deteccion
                        datos_threatDetail['rango_alcance'] = 100
                        datos_threatDetail['threat_id'] = threat_id
                        datos_threatDetail['expiracion'] = "20170323"
                        datos_threatDetail['typeCrop_id'] = request.POST['crop_id']
                        serializer = ThreatDetailSerializer(data=datos_threatDetail)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError

                else:
                    # agregar la amenaza inactiva porque un admin debe activarla
                    datos_threat['movil_id'] = request.POST['movil_id']
                    datos_threat['name'] = request.POST['name']
                    datos_threat['scientific_name'] = request.POST['scientific_name']
                    datos_threat['typeThreat_id'] = request.POST['typeThreat_id']
                    datos_threat['active'] = False
                    datos_threat['wikipedia_link'] = "info wiki"
                    datos_threat['description'] = request.POST['scientific_name']
                    threat_cant = Threat.objects.filter().count()
                    datos_threat['code'] = threat_cant + 1
                    #agregar la amenaza inactiva porque un admin debe activarla

                    serializer = ThreatSerializer(data=datos_threat)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise AttributeError


            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pruebaPush(tipo,amenaza_id):

    data_message = {"type": tipo, "threat_id": amenaza_id, "cantidad": 55}

    amenaza = Threat.objects.get(id=amenaza_id)
    nombre_amenaza = amenaza.name
    #print nombre_amenaza
    dispositivos = Device.objects.filter(active=True)
    for objectDevice in dispositivos:
       key_firebase = objectDevice.key_firebase
       #print key_firebase
       title = "Se aproximan " + nombre_amenaza
       body = " nuevas detecciones en tu zona"
       resultado = push_notifications_view(key_firebase, title, body,data_message)
       print resultado


    return Response({"success": ("GUARDA TODO deteccion")}, status=status.HTTP_200_OK)


##### DETECCION
##################################
# Agrega y modifica actividades de lote

@api_view(['POST', 'GET'])
def detection(request):
    if request.method == 'POST':
       try:
           with transaction.atomic():
               datos_detection = {}
               datos_note = {}

               movil_id = request.POST['movil_id']

               datos_detection['user_id'] = request.user.id
               datos_detection['movil_id'] = movil_id
               datos_detection['date'] = request.POST['date']
               datos_detection['damage_level'] = request.POST['damage_level']
               datos_detection['threatDetail_id'] = request.POST['threat_id']

               datos_note['user_id'] = request.user.id
               datos_note['object_id'] = movil_id
               datos_note['object_type'] = "Detection"
               datos_note['content'] = request.POST['note']

               import json
               actividades = request.POST['activity_id']
               actividades2 = actividades.replace("\\" ,"")
               actividades_json = json.loads(actividades2)


               for registroActividad in actividades_json:
                   
		   activity_id = registroActividad['id']
                   datos_detection['activity_id'] = activity_id
                   datos_detection['location_lat'] = registroActividad['location_lat']
                   datos_detection['location_long'] = registroActividad['location_long']

		   existen=0
                   if(activity_id == 0):
                       #existen = 0
		       existen = Detection.objects.filter(movil_id=movil_id, location_lat=datos_detection['location_lat'] ,location_long=datos_detection['location_long']).count()
                   else:
                       existen = Detection.objects.filter(movil_id=movil_id,activity_id=activity_id).count()
                   
                   if (existen == 0):
                        serializer = DetectionSerializer(data=datos_detection)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
                   	
			nota(datos_note)
                        image(request)
                        # PUSH envio notificacion
                        push(datos_detection['threatDetail_id'])
		   else:
			return Response({"success": ("Ya existe deteccion")}, status=status.HTTP_200_OK)
                        #ACTUALIZO
                        #detection = Detection.objects.filter(movil_id=movil_id,activity_id=activity_id)
                        #for objectDetection in detection:
                            #serializer = DetectionSerializer(objectDetection, data=datos_detection)
                            #if serializer.is_valid():
                               # serializer.save()
                            #else:
                                #raise AttributeError

               #nota(datos_note)
               #image(request)
               #PUSH envio notificacion
               #push(datos_detection['threatDetail_id'])


           return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
       except (AttributeError, ObjectDoesNotExist):
              pass
              return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        detections = Detection.objects.filter()
        serializer = DetectionSerializer(detections, many=True)
        return JSONResponse(serializer.data)

def push(amenaza_id):
    #actividad = Activity.objects.get(movil_id=activity_id)
    #crop = TypeCrop.objects.get(id=actividad.type_crop_id)
    #cultivo = crop.name

     
    cantidad = Detection.objects.filter(threatDetail_id=amenaza_id)
    cantidad = cantidad.count()
    
    data_message = {"type" : 1, "threat_id":amenaza_id,"cantidad":cantidad}
    

    amenaza = Threat.objects.get(id=amenaza_id)
    nombre_amenaza = amenaza.name
    #print nombre_amenaza
    dispositivos = Device.objects.filter(active=True)
    for objectDevice in dispositivos:
       key_firebase = objectDevice.key_firebase
       #print key_firebase

       title = "Se aproxima " + nombre_amenaza 
       #str("!") 
       body =  "nuevas detecciones en tu zona"
       resultado = push_notifications_view(key_firebase, title, body,data_message)
       print resultado   
   
   

def nota(datos_note):
    object_id = datos_note['object_id']
    existeNota = Note.objects.filter(object_id=object_id).count()
    if (existeNota == 0):
        serializerNote = NoteSerializer(data=datos_note)
        if serializerNote.is_valid():
            serializerNote.save()
        else:
            raise AttributeError
    else:
        # ACTUALIZO
        detection = Detection.objects.filter(movil_id=object_id)
        for objectNote in detection:
            serializer = DetectionSerializer(objectNote, data=datos_note)
            if serializer.is_valid():
                serializer.save()
            else:
                raise AttributeError


def image(request):
    request.POST['object_id'] = request.POST['movil_id']
    request.POST['object_type'] = "Detection"
    object_id = request.POST['movil_id']
    object_type = request.POST['object_type']	
    #imagen = request.FILES['image']
    #print "aca"+imagen

    existeImage = Picture.objects.filter(object_id=object_id,object_type=object_type).count()
    if (existeImage == 0):
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise AttributeError
    else:
            # ACTUALIZO
            picture = Picture.objects.filter(object_id=object_id,object_type=object_type)
            for objectImage in picture:
                serializer = PictureSerializer(objectImage, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise AttributeError


#detection-user
@api_view(['GET'])
def detectionUser(request):
    if request.method == 'GET':

        list_detection = []
        image_url = "sin imagen"
        note="sin comentario"
        va = 3
        list_activity = []

        detections = Detection.objects.filter(user_id=request.user.id)
        for objectDetection in detections:
            notes = Note.objects.filter(user_id=request.user.id, object_id=objectDetection.movil_id,object_type="Detection")
            for objectNote in notes:
               	note = objectNote.content


            picture = Picture.objects.filter(object_id=objectDetection.movil_id)
            for objectPicture in picture:
                image = str(objectPicture.image)
                if(image != ""):
                    image_url = settings.MEDIA_URL + image
                else:
                    image_url = "sin imagen"
		#image_url = settings.MEDIA_URL + image
	

            activity_id = objectDetection.activity_id
            activites = Activity.objects.filter(user_id=request.user.id,movil_id=activity_id)
            for objectActivity in activites:
                activity_movil_id = objectActivity.movil_id
                dato_activity = {"activity_movil_id": activity_movil_id }
                list_activity.append(dato_activity)


            dato = {
                "movil_id": objectDetection.movil_id,
                "date": objectDetection.date,
                "threat_id": objectDetection.threatDetail_id,
                "note": note,
                "user_id": objectDetection.user_id,
                "image": image_url,
                "index_va":va,
                "activites": list_activity
            }
            list_activity = []
            list_detection.append(dato)

        return JSONResponse(list_detection)



@api_view(['GET'])
def detectionThreat(request,threat_id):
    if request.method == 'GET':

        list_detection = []
        image_url = "sin imagen"
        note = "sin comentario"
        sum_seen= 0
        sum_note = 0
        user = ""
        center_lat = 0
        center_long = 0

        detections = Detection.objects.filter(threatDetail_id=threat_id)
        for objectDetection in detections:
  	    image_url = "sin imagen"
            note = "sin comentario"
            sum_seen= 0
            sum_note = 0
            user = ""
            center_lat = 0
            center_long = 0

	    perfil = Profile.objects.filter(user_id=objectDetection.user_id)
            for objectPerfil in perfil:
               	user = str(objectPerfil.name)

            if(user == ""):
                usuario = UserModel.objects.filter(id=objectDetection.user_id)
                for objectUser in usuario:
                    user = str(objectUser.username)	    

	    notes = Note.objects.filter(user_id=objectDetection.user_id, object_id=objectDetection.movil_id,object_type="Detection")
            for objectNote in notes:
                note = objectNote.content
	        sum_note = sum_note + 1

	    picture = Picture.objects.filter(object_id=objectDetection.movil_id)
            for objectPicture in picture:
                image = str(objectPicture.image)
                if(image != ""):
                    image_url = settings.MEDIA_URL + image
                else:
                    image_url = "sin imagen"

	    activites = Activity.objects.filter(movil_id=objectDetection.activity_id)
            for objectActivity in activites:
                parcels = Parcel.objects.filter(movil_id=objectActivity.parcel_id)
                for objectParcel in parcels:
                    center_lat = objectParcel.center_lat
                    center_long = objectParcel.center_long

            seens = Seen.objects.filter(object_id=threat_id,object_type="threat")
            for objectSeen in seens:
                sum_seen = sum_seen + 1

            dato = {
                    "movil_id": objectDetection.movil_id,
                    "date": objectDetection.date,
                    "damage_level": objectDetection.damage_level,
                    "threat_id": objectDetection.threatDetail_id,
                    "note": note,
                    "user": user,
                    "image": image_url,
                    "center_lat": center_lat,
                    "center_long": center_long,
                    "seen_sum": sum_seen,
                    "note_sum": sum_note
            }
            list_detection.append(dato)
	    sum_note = 0
            sum_seen = 0

        return JSONResponse(list_detection)


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all().order_by()
    serializer_class = PictureSerializer

# return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)
#Vista agregar y modificar deteccion y detalle



##### VISTOS
##################################
# Agrega y modifica actividades de lote
@api_view(['POST', 'GET'])
def seen(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for registro in request.data:
                    registro['user_id'] = request.user.id
                    #('user_id', 'object_id', 'object_type', 'date_time')
                    existeImage = Seen.objects.filter(object_id=registro['object_id'],object_type=registro['object_type'],user_id=registro['user_id']).count()
                    if (existeImage == 0):
                        serializer = SeenSerializer(data=registro)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            raise AttributeError
                    else:
			continue
                        #turn Response({"success": ("Ya existe")}, status=status.HTTP_200_OK)
			# ACTUALIZO
                        #detection = Detection.objects.filter(object_id=registro['object_id'],object_type=registro['object_type'],user_id=registro['user_id'])
                        #for objectNote in detection:
                            #serializer = DetectionSerializer(objectNote, data=registro)
                            #if serializer.is_valid():
                                #serializer.save()
                            #else:
                                #raise AttributeError
			
            return Response({"success": ("GUARDA TODO")}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({"error": ("NO GUARDA NADA")}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        seens = Seen.objects.filter()
        serializer = SeenSerializer(seens, many=True)
        return JSONResponse(serializer.data)



@api_view(['GET'])
def seenUser(request):
    if request.method == 'GET':
        seens = Seen.objects.filter(user_id=request.user.id)
        serializer = SeenSerializer(seens, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
def detectionRadio(request, lat, long):
        if request.method == 'GET':
            #print lat
            #print long
            #seens = Seen.objects.filter(user_id=id)
            #serializer = SeenSerializer(seens, many=True)

            detections = Detection.objects.filter()
	    cantidad = detections.count()

            return JSONResponse(cantidad)

