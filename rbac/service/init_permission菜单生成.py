from django.conf import settings
def init_permission(request, user):
    """权限和信息初始化，以后使用时，需要在登录成功后调用该方法讲权限和菜单信息放入session"""
    permission_queryset = user.roles.filter(permissions__url__isnull=False).values(
        'permissions__url',
        'permissions__title',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    ).distinct()

    menu_dict = {}
    permission_list = []

    for row in permission_queryset:
        permission_list.append({'permissions_url': row['permissions__url']})
        menu_id = row.get('permissions__menu_id')
        if not menu_id:
            continue
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': row['permissions__menu__title'],
                'icon': row['permissions__menu__icon'],
                'children': [
                    {'title': row['permissions__title'], 'url': row['permissions__url']}
                ]
            }
        else:
            menu_dict[menu_id]['children'].append({'title': row['permissions__title'],
                                                   'url': row['permissions__url']})

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict

