from django.conf.urls import url
from account import views
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
]