from django.conf.urls import url

from report import views

urlpatterns = [
    url(r'^produce/$', views.report_produce, name='report_produce'),
    url(r'^device/$', views.report_device, name='report_device'),
    url(r'^mold/$', views.report_mold, name='report_mold'),
    url(r'^quality/$', views.report_quality, name='report_quality'),
]