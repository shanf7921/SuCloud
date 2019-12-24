from django.conf.urls import url
from alarm import views
urlpatterns = [
    url(r'^rule/$', views.alarm_rule, name='alarm_rule'),
    url(r'^warm/$', views.alarm_warm, name='alarm_warm'),
    url(r'^record/$', views.alarm_record, name='alarm_record'),

]