from django.test import TestCase

# Create your tests here.
import os
if __name__ == "__main__":
    # 设置Django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'SuCloud.settings')
    import django
    django.setup()

    from rbac.models import UserInfo
    name = '塑云2号'
    obj = UserInfo.objects.filter(uname=name).first()
    # 查询当前用户的所有角色
    role = obj.roles.all()
    permissions_list = []
    for i in role:
        # 查看当前用户所有角色的所有权限
        per = i.permissions.all()
        for j in per:
            permissions_list.append(j.url)

    print(permissions_list)