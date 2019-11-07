from django.contrib import admin
from device.models import DeviceMd
# Register your models here.
class DeviceMdAdmin(admin.ModelAdmin):
    list_display = ("d_num", "d_brank", "d_name", "d_status", "d_created")
    list_filter = ("d_brank", "d_name", "d_status")
    search_fields = ("d_brank", "d_name", "d_status")
    ordering = ["-d_created"]


admin.site.register(DeviceMd, DeviceMdAdmin)