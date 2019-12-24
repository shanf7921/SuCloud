from django.conf.urls import url
from rbac import views
urlpatterns = [
    url(r'^permission/$', views.permission, name='permission'),
    url(r'^user/$', views.user, name='user'),

]