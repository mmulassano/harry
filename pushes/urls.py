from django.conf.urls import include, url
from pushes import views

urlpatterns = [
    #url(r'^push/$', views.push_notifications_view),
   url(r'^device/$', views.device)
]
