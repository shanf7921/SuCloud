from django.conf.urls import url
from mold import views
urlpatterns = [
    url(r'^list/$', views.mold_list, name='mold_list'),
    url(r'^maintain/$', views.mold_maintain, name='mold_maintain'),
    url(r'^record/$', views.mold_record, name='mold_record'),

]