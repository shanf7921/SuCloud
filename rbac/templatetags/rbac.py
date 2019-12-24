from django.template import Library
from django.conf import settings
import re
from collections import OrderedDict
register =Library()

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """生成菜单"""
    # 获取session中的菜单列表
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    # 实列化
    ordered_dict = OrderedDict()
    for key in sorted(menu_dict):
        # 对字典的key做排序，并添加到有序字典对象中
        ordered_dict[key] = menu_dict[key]

        # 循环二级菜单
        for node in menu_dict[key]['children']:
            # 每一个url增加^$, 比如 /device/list/ 变成 ^/device/list/$
            reg = "^%s$" % node['url']
            # 判断当前路径是否匹配
            if re.match(reg, request.path_info):
                # 增加一个样式，class为action，表示选中状态.这是给前端展示用的
                node['class'] = 'active'



    # 变量传给模板(如果前端导航顺序出错，就去掉下行注释)
    # return {'menu_dict': ordered_dict}
    return {'menu_dict': menu_dict}

