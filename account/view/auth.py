from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rbac.models import UserInfo
from rbac.service.init_permission import init_permission
from utils.response import BaseResponse
from django.contrib.auth.models import User
# 验证登录是否成功
from django.contrib.auth import authenticate, login
class AuthView(ViewSetMixin, APIView):
    authentication_classes = []
    def login(self, request, *args, **kwargs):
        """用户登陆认证"""
        response = BaseResponse()
        try:
            username = request.data.get('username')
            pwd = request.data.get('password')
            # 验证用户和密码
            user = authenticate(username=username, password=pwd)
            # obj = User.objects.filter(username=user).first()
            # obj = User.objects.get(username=user)
            # uclass = UserInfo.objects.get(user=obj)
            # print(type(uclass)) 输出结果如下，所以此步 定义为uclass
            # <class 'rbac.models.UserInfo'>
            if not user:
                # 判断查询结果
                response.code = 1002
                response.error = '用户名或密码错误'
            else:
                login(request, user)
                uclass = UserInfo.objects.get(user=user)
                obj = UserInfo.objects.filter(user_id=uclass.user_id).first()
                # 查询当前用户的所有角色
                role = obj.roles.all()
                # 定义空列表
                permission_list = []
                for i in role:
                    # 查看当前用户所有角色的所有权限
                    per = i.permissions.all()
                    for j in per:
                        permission_list.append(j.url)
                response.code = 1000

                # 增加session
                request.session['url'] = permission_list
                init_permission(request, obj)
        except Exception as e:
            response.code = 10005
            response.error = '操作异常'
        return Response(response.dict)
