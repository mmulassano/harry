from django.conf.urls import url
from alertas import views


urlpatterns = [
    #url(r'^farm/$', views.farm),
    url(r'^threat/$', views.threat),
    url(r'^detection/$', views.detection),
    url(r'^image/$', views.image),
    url(r'^seen/$', views.seen),
    url(r'^detection-user/$', views.detectionUser),
    url(r'^detection-threat/(?P<threat_id>[0-9]+)$', views.detectionThreat),
    url(r'^seen-user/$', views.seenUser),
    #url(r'^detection-radio/(?P<lat>[0-9]+)/(?P<long>[0-9]+)$', views.detectionRadio)
    url(r'^detection-radio/(?P<lat>.*)/(?P<long>.*)/$', views.detectionRadio),
    #rl(r'^prueba-push/(?P<tipo>[0-9]+)/(?P<amenaza_id>[0-9]+)/$', views.pruebaPush),
    url(r'^prueba-push/(?P<tipo>.*)/(?P<amenaza_id>.*)/$', views.pruebaPush),
    url(r'^threat-new/$', views.threatNew)
]
