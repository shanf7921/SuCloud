from django.contrib import admin
from mold.models import Mold


class MoldAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['m_num', 'm_name', 'm_count', 'm_life', 'm_product', 'm_status', 'm_user']
    # 允许编辑
    list_editable = ['m_name', 'm_status']
    # 过滤器
    list_filter = ['m_status', 'm_user']


admin.site.register(Mold, MoldAdmin)



