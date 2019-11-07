from django.conf.urls import url
from device import views
urlpatterns = [
    url(r'^list/$', views.device_list, name='device_list'),
]