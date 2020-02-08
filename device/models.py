from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class DeviceMd(models.Model):
    d_type_choice = (('1', u'注塑机'), ('2', u'辅机'))
    d_status_choice = (('1', u'运行'), ('2', u'待机'), ('3', u'离线'))
    d_type = models.CharField(max_length=100, choices=d_type_choice, verbose_name="设备类型")
    d_num = models.CharField(max_length=100, unique=True, verbose_name="设备编号")
    d_brank = models.CharField(max_length=100, blank=True, verbose_name="设备品牌")
    d_model = models.CharField(max_length=100, blank=True, verbose_name="设备型号")
    d_name = models.CharField(max_length=100, blank=True, verbose_name="设备名称")
    d_status = models.CharField(max_length=100, choices=d_status_choice, verbose_name="设备状态")
    d_user = models.ForeignKey(User, related_name="device_adds", verbose_name="添加人员")
    d_created = models.DateTimeField(default=timezone.now, verbose_name="添加时间")
    d_photo = models.ImageField(upload_to='image/%Y/%m/%d', blank=True, verbose_name="设备图片")

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备"

    def __str__(self):
        return self.d_num

class DeviceRepair(models.Model):
    dr_num = models.ForeignKey(DeviceMd, related_name="repair")
    dr_start = models.CharField(max_length=100, blank=True, verbose_name="开始时间")
    dr_end = models.CharField(max_length=100, null=True, blank=True, verbose_name="结束时间")
    dr_user = models.CharField(max_length=100, blank=True, verbose_name="维修人员")
    dr_des = models.CharField(max_length=300, blank=True, verbose_name="备注")




