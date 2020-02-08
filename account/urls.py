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
    url(r'^change-permission/$', views.change_permission, name='change_permission'),
    url(r'^get-permission/$', views.get_permission, name='get_permission'),
    url(r'^rule-change/$', views.rule_change, name='rule_change'),
    url(r'^add-device-repair/$', views.add_device_repair, name='add_device_repair'),
    url(r'^add-order/$', views.add_order, name='add_order'),
    url(r'^edit-order/$', views.edit_order, name='edit_order'),
    url(r'^order-dispense/$', views.order_dispense, name='order_dispense'),
    url(r'^add-device/$', views.add_device, name='add_device'),
    url(r'^change-status/$', views.change_status, name='change_status'),

]