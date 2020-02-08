from django.conf.urls import url
from device import views
urlpatterns = [
    url(r'^list/$', views.device_list, name='device_list'),
    url(r'^status/$', views.device_status, name='device_status'),
    url(r'^maintain/$', views.device_maintain, name='device_maintain'),
]