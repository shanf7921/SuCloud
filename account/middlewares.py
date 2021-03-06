from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from SuCloud import settings
import os

class AuthMD(MiddlewareMixin):
    # 白名单
    white_list = ['/', '/login/', '/auth/', '/admin/login/', '/admin/', '/account/login/']
    # 黑名单
    black_list = []
    # 默认状态
    ret = {"status": 0, 'url': '', 'msg': ''}

    def process_request(self, request):
        # 获取请求路径
        request_url = request.path_info
        # get_full_path() 表示带参数的路径
        # print(request.path_info, request.get_full_path())

        # 判断请求路径不在白名单中
        if request_url not in self.white_list:
            import re
            # 获取用户session中的url列表
            per_url = request.session.get("url")
            if per_url:
                for i in per_url:
                    # 使用正则匹配，其中i为正则表达式,request_url.lstrip('/')表示去除左边的'/'
                    # result = re.match(i, request_url.lstrip('/'))
                    result = re.match(i, request_url)
                    if result:
                        print('授权通过', request_url)
                        # return None 表示可以继续走下面的流程
                        return None
                    else:
                        # print('授权不通过', request_url)
                        pass

            # 错误页面提示
            self.ret['msg'] = '未授权，禁止访问'
            self.ret['url'] = "/login/"
            path = os.path.join(settings.BASE_DIR, 'account/templates/error.html')
            return render(request, path, self.ret)

