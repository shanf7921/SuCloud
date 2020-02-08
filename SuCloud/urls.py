"""SuCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# 登录相关
from account.view import login, auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls', namespace="account", app_name="account")),
    url(r'^device/', include('device.urls', namespace="device", app_name="device")),

    # 登录相关
    url(r'^$', login.login),
    url(r'^login/$', login.login, name='login'),
    url(r'^auth/$', auth.AuthView.as_view({'post': 'login'})),

    # 系统管理方面(用户管理，权限管理 放在rbac内进行处理)
    url(r'^system/', include('rbac.urls', namespace="system", app_name="system")),
    # 模具管理
    url(r'^mold/', include('mold.urls', namespace="mold", app_name="mold")),
    # 报警管理
    url(r'^alarm/', include('alarm.urls', namespace="alarm", app_name="alarm")),
    # 工单管理
    url(r'^produce/', include('produce.urls', namespace="produce", app_name="produce")),
    # 看板管理
    url(r'^kanban/', include('kanban.urls', namespace="kanban", app_name="kanban")),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)