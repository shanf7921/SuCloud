from django.conf.urls import url
from produce import views
urlpatterns = [
    url(r'^order/$', views.produce_order, name='produce_order'),
    url(r'^dispense/$', views.produce_dispense, name='produce_dispense'),
    url(r'^speed/$', views.produce_speed, name='produce_speed'),
]
