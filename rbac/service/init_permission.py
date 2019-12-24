from django.conf import settings
def init_permission(request, user):
    """权限和信息初始化，以后使用时，需要在登录成功后调用该方法讲权限和菜单信息放入session"""
    # 获取用户信息和权限信息写入session
    permission_queryset = user.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    ).distinct()

    # 菜单字典，它是能成为菜单的权限，用于做菜单显示
    menu_dict = {}
    # 权限列表，多有权限，用于做权限校验
    permission_list = []

    for row in permission_queryset:
        permission_list.append({'permissions_url': row['permissions__url']})

        # 获取菜单id
        menu_id = row.get('permissions__menu_id')
        # 如果菜单id为空，则跳过此次循环
        if not menu_id:
            continue

        # 判断菜单id不在字典里面时，避免一级菜单重复
        if menu_id not in menu_dict:
            # 以菜单id为key
            menu_dict[menu_id] = {
                # value部分就是title，用来展示一级菜单
                'title': row['permissions__menu__title'],
                # 一级菜单的图标
                'icon': row['permissions__menu__icon'],
                # 二级菜单
                'children': [
                    # 二级菜单标题url(注意：一级菜单是不能点击的，所以它没有url)
                    # 二级菜单是可以点击的，但是它没有图标
                    {'title': row['permissions__title'], 'url': row['permissions__url']}
                ]
            }
        else:
            # 如果一级菜单还有二级菜单，就继续添加
            menu_dict[menu_id]['children'].append({'title': row['permissions__title'], 'url': row['permissions__url']})

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict

