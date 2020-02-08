from django.conf.urls import url
from kanban import views
urlpatterns = [
    url(r'^produce/$', views.kanban_produce, name='kanban_produce'),
    url(r'^device/$', views.kanban_device, name='kanban_device'),
    url(r'^order/$', views.kanban_order, name='kanban_order'),

]