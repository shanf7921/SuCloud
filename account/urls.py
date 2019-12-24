from django.conf.urls import url
from django.contrib.auth import views as auth_views
from account import views
urlpatterns = [
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', views.register, name='user_register'),
    url(r'^logout/$', auth_views.logout, {"template_name": "login.html"}, name="user_logout"),
    url(r'^del-device/$', views.del_device, name='del_device'),
    url(r'^del-mold/$', views.del_mold, name='del_mold'),
    url(r'^mold-repair/$', views.mold_repair, name='mold_repair'),
    url(r'^mold-maintain/$', views.mold_maintain, name='mold_maintain'),
    url(r'^mold-end/$', views.mold_end, name='mold_end'),
    url(r'^del-rule/$', views.del_rule, name='del_rule'),
    url(r'^add-rule/$', views.add_rule, name='add_rule'),

]