data = [
    {'permissions__menu_id': 1, 'permissions__url': '/customer/list/', 'permissions__title': '客户列表', 'permissions__menu__title': '信息管理', 'permissions__menu__icon': 'fa-coffee'},
    {'permissions__menu_id': None, 'permissions__url': '/customer/add/', 'permissions__title': '添加客户', 'permissions__menu__title': None, 'permissions__menu__icon': None},
    {'permissions__menu_id': 1, 'permissions__url': '/payment/list/', 'permissions__title': '账单列表', 'permissions__menu__title': '信息管理', 'permissions__menu__icon': 'fa-coffee'},
]
dict = [{'1':
             {'title': '现场看板', 'icon': '',
              'children': [{'title': '生产看板', 'url': '/kanban/produce/'},
                           {'title': '设备看板', 'url': '/kanban/device/'},
                           {'title': '订单看板', 'url': '/kanban/order/'}]},
         '2': {'title': '设备管理', 'icon': '',
               'children': [{'title': '设备台账', 'url': '/device/list/'},
                            {'title': '设备状态', 'url': '/device/status/'},
                            {'title': '设备维保', 'url': '/device/maintain/'}]}
         }
        ]
dict2 = {1:
     {'title': '信息管理', 'icon': 'fa-coffee',
     'children': [{'title': '客户列表', 'url': '/customer/list/'},
                  {'title': '账单列表', 'url': '/payment/list/'}]}
 }


menu_dict={}  # 菜单字典

for row in data:
    # 获取菜单id
    menu_id = row.get('permissions__menu_id')
    # 如果菜单id为空,跳过此次循环
    if not menu_id:
        continue

    # 判断菜单id不在字典里面时,避免一级菜单重复
    if menu_id not in menu_dict:
        # 以菜单id为key
        menu_dict[menu_id] = {
            # value部分就是title,用来展示一级菜单
            'title':row['permissions__menu__title'],
            # 一级菜单的图标
            'icon':row['permissions__menu__icon'],
            # 二级菜单
            'children':[
                # 二级菜单标题和url。注意:一级标题是不能点击的,所以它没有url
                # 二级菜单是可以点击的,但是它没有图标
                {'title':row['permissions__title'],'url':row['permissions__url']}
            ]
        }
    else:
        # 如果一级菜单还有二级菜单,就继续添加
        menu_dict[menu_id]['children'].append({'title': row['permissions__title'], 'url': row['permissions__url']})

print(menu_dict)
