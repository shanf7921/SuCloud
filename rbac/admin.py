from django.contrib import admin
from rbac.models import Menu, Permission, Role, UserInfo
# Register your models here.
admin.site.register(Menu)

class PermissionAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['title', 'url']
    # 允许编辑
    list_editable = ['url']
    # 过滤器
    list_filter = ['menu']
admin.site.register(Permission, PermissionAdmin)



class RoleAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
admin.site.register(Role, RoleAdmin)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'uname', 'email', 'phone']
    filter_horizontal = ['roles']
admin.site.register(UserInfo, UserInfoAdmin)