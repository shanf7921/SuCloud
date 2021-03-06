from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, HttpResponse
import re

from account.view.auth import AuthView
from rbac.service.init_permission import init_permission


class RbacMiddleware(MiddlewareMixin):
    """
    权限控制的中间件
    """

    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1. 获取当前请求URL
        current_url = request.path_info

        # 1.5 白名单处理
        for reg in settings.VALID_URL:
            if re.match(reg, current_url):
                return None
        AuthView()
        # 2. 获取当前用户session中所有的权限
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return redirect('/login/')

        # 3. 进行权限校验
        flag = False
        for item in permission_list:
            reg = "^%s$" %(item.get('permissions_url'))
            if re.match(reg, current_url):
                flag = True
                break
        if not flag:
            if permission_list:
                url = permission_list[0]['permissions_url']
                return redirect(url)
            else:
                return HttpResponse('无权访问')
