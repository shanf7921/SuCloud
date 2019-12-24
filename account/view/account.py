from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo
from django.conf import settings
from django.contrib.auth.models import User
from rbac.service import init_permission


def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    print('account/view/account.py')
    if request.method == 'GET':
        return render(request, 'login.html')

    # 1. 获取提交的用户名和密码
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    # 2. 检验用户是否合法
    obj = User.objects.filter(name=user, password=pwd).first()
    if not obj:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    # 3. 获取用户信息和权限信息写入session
    # uclass = UserInfo.objects.get(user=obj)
    uclass = UserInfo.objects.get(user=obj)
    obj = UserInfo.objects.filter(user_id=uclass.user_id).first()
    """
    有些用户是没有角色的。需要使用permissions__url__isnull=False 过滤掉为空的记录
    由于权限判断，只需要url,所以取url字段，也就是values('permissions__url')
    由于用户可能有多个角色，那么url必然有重复的，使用distinct()去重。
    
    在django中session存储时，默认对数据做序列化。所以数据不要是queryset对象，使用list进行强制转换！
    权限在很多地方会用到，为了避免key变动，导致代码改动。将key放在settings.py中
    """

    # permission_queryset = obj.roles.filter(permissions__url__isnull=False).values(
    #     'permissions__url', 'permissions__is_menu', 'permissions__title', 'permissions__icon').distinct()
    # # request.session['user_info'] = {'id': obj.id, 'name': obj.name}
    # # request.session[settings.PERMISSION_SESSION_KEY] = list(permission_list)
    #
    # # 菜单列表
    # menu_list = []
    # # 权限列表
    # permission_list = []
    #
    # for row in permission_queryset:
    #     permission_list.append({'permissions__url': row['permissions__url']})
    #     if row['permissions__is_menu']:
    #         menu_list.append({'title': row['permissions__title'], 'icon': row['permissions__icon'], 'url': row['permissions__url']})
    #
    # request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # request.session[settings.MENU_SESSION_KEY] = menu_list
    init_permission(request, obj)
    return redirect('/device/list/')
