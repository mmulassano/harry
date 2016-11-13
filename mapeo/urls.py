
from django.conf.urls import url
from mapeo import views


urlpatterns = [
    #url(r'^farm/$', views.farm),
    url(r'^farmDelete/$', views.farmDelete),
    url(r'^farm/$', views.farm),
    url(r'^parcelDelete/$', views.parcelDelete),
    url(r'^parcel/$', views.parcel),
    url(r'^activity/$', views.activity),
    url(r'^activityDelete/$', views.activityDelete),
    url(r'^campaign/$', views.list_campaign),
    url(r'^parcelFarm/(?P<farm_id>[0-9]+)$', views.parcelFarm)
]
