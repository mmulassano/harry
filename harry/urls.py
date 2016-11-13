"""harry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from usuario.views import UserViewSet,GroupViewSet,TypeUserViewSet,ProfileViewSet
from mapeo.views import TypeCropViewSet, PostViewSet
from alertas.views import TypeThreatViewSet,ThreatViewSet,PictureViewSet, NoteViewSet
from location import views
#from pushes.views import DeviceViewSet
import settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'type-user', TypeUserViewSet)
router.register(r'picture', PictureViewSet)
router.register(r'note', NoteViewSet)

router.register(r'posts', PostViewSet)
#router.register(r'farm', FarmViewSet)
router.register(r'type-crop', TypeCropViewSet)
router.register(r'type-threat', TypeThreatViewSet)
router.register(r'profile', ProfileViewSet)


#router.register(r'device', DeviceViewSet)
#router.register(r'threat', ThreatViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('alertas.urls')),
    url(r'^', include('mapeo.urls')),
    url(r'^', include(router.urls)),
    url(r'^location/', views.location),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^', include('pushes.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    })
]
