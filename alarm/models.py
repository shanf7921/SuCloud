from django.db import models
from django.utils import timezone
# Create your models here.
from device.models import DeviceMd

# 参数实时记录表
class ParamTime(models.Model):
    t_device = models.ForeignKey(DeviceMd, related_name="paramtime")
    t_all = models.FloatField(default=0, verbose_name="循环时间", null=True)
    t_open_mold = models.FloatField(default=0, null=True)
    t_close_mold = models.FloatField(default=0, null=True)
    t_stock = models.FloatField(default=0, verbose_name="储料时间", null=True)
    t_ejection = models.FloatField(default=0, verbose_name="射出时间", null=True)
    t_back = models.FloatField(default=0, verbose_name="射退时间", null=True)
    t_change = models.FloatField(default=0, verbose_name="转保压时间", null=True)

    t_change_place = models.FloatField(default=0, verbose_name="转保压位置", null=True)
    t_change_pressure = models.FloatField(default=0, verbose_name="转保压压力", null=True)

    t_tem1 = models.FloatField(default=0, null=True)
    t_tem2 = models.FloatField(default=0, null=True)
    t_tem3 = models.FloatField(default=0, null=True)
    t_tem4 = models.FloatField(default=0, null=True)
    t_tem5 = models.FloatField(default=0, null=True)

    t_open_place = models.FloatField(default=0, null=True)
    t_ejection1 = models.FloatField(default=0, verbose_name="射出起点", null=True)
    t_ejection2 = models.FloatField(default=0, verbose_name="射出终点", null=True)
    t_created = models.DateTimeField(default=timezone.now, verbose_name="添加时间", null=True)
    t_error = models.BooleanField(default=False)

# 参数设定表
class ParamSet(models.Model):
    t_device = models.ForeignKey(DeviceMd, related_name="paramset")

    s_open_place1 = models.FloatField(default=0, verbose_name="开模一段位置", null=True)
    s_open_pressure1 = models.FloatField(default=0, verbose_name="开模一段压力", null=True)
    s_open_speed1 = models.FloatField(default=0, verbose_name="开模一段速度", null=True)
    s_open_place2 = models.FloatField(default=0, verbose_name="开模二段位置", null=True)
    s_open_pressure2 = models.FloatField(default=0, verbose_name="开模二段压力", null=True)
    s_open_speed2 = models.FloatField(default=0, verbose_name="开模二段速度", null=True)
    s_open_place3 = models.FloatField(default=0, verbose_name="开模三段位置", null=True)
    s_open_pressure3 = models.FloatField(default=0, verbose_name="开模三段压力", null=True)
    s_open_speed3 = models.FloatField(default=0, verbose_name="开模三段速度", null=True)
    s_open_place4 = models.FloatField(default=0, verbose_name="开模四段位置", null=True)
    s_open_pressure4 = models.FloatField(default=0, verbose_name="开模四段压力", null=True)
    s_open_speed4 = models.FloatField(default=0, verbose_name="开模四段速度", null=True)
    s_open_place5 = models.FloatField(default=0, verbose_name="开模五段位置", null=True)
    s_open_pressure5 = models.FloatField(default=0, verbose_name="开模五段压力", null=True)
    s_open_speed5 = models.FloatField(default=0, verbose_name="开模五段速度", null=True)

    t_open_mold = models.FloatField(default=0, verbose_name="开模时间", null=True)
    t_close_mold = models.FloatField(default=0, verbose_name="关模时间", null=True)
    t_stock = models.FloatField(default=0, verbose_name="储料时间", null=True)
    t_ejection = models.FloatField(default=0, verbose_name="射出时间", null=True)
    t_back = models.FloatField(default=0, verbose_name="射退时间", null=True)
    t_change = models.FloatField(default=0, verbose_name="转保压时间", null=True)

    t_change_place = models.FloatField(default=0, verbose_name="转保压位置", null=True)
    t_change_pressure = models.FloatField(default=0, verbose_name="转保压压力", null=True)

    t_tem1 = models.FloatField(default=0, null=True)
    t_tem2 = models.FloatField(default=0, null=True)
    t_tem3 = models.FloatField(default=0, null=True)
    t_tem4 = models.FloatField(default=0, null=True)
    t_tem5 = models.FloatField(default=0, null=True)

    t_open_place = models.FloatField(default=0, null=True)
    t_ejection1 = models.FloatField(default=0, verbose_name="射出起点", null=True)
    t_ejection2 = models.FloatField(default=0, verbose_name="射出终点", null=True)
    t_created = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

# 参数容错表
"""
class ParamError(models.Model):
    t_device = models.ForeignKey(DeviceMd, related_name="paramerror")
    t_all = models.FloatField(blank=True, verbose_name="循环时间")
    t_open_mold = models.FloatField(blank=True,)
    t_close_mold = models.FloatField(blank=True,)
    t_stock = models.FloatField(blank=True, verbose_name="储料时间")
    t_ejection = models.FloatField(blank=True, verbose_name="射出时间")
    t_back = models.FloatField(blank=True, verbose_name="射退时间")
    t_change = models.FloatField(blank=True, verbose_name="转保压时间")

    t_change_place = models.FloatField(blank=True, verbose_name="转保压位置")
    t_change_pressure = models.FloatField(blank=True, verbose_name="转保压压力")

    t_tem1 = models.FloatField(blank=True,)
    t_tem2 = models.FloatField(blank=True,)
    t_tem3 = models.FloatField(blank=True,)
    t_tem4 = models.FloatField(blank=True,)
    t_tem5 = models.FloatField(blank=True,)

    t_open_place = models.FloatField(blank=True,)
    t_ejection1 = models.FloatField(blank=True, verbose_name="射出起点")
    t_ejection2 = models.FloatField(blank=True, verbose_name="射出终点")
    t_created = models.DateTimeField(default=timezone.now, verbose_name="添加时间")
"""


# 参数容错表
class ParamError(models.Model):
    t_device = models.ForeignKey(DeviceMd, related_name="paramerror")

    e_time = models.FloatField(blank=True, null=True, verbose_name="时间")
    e_tem = models.FloatField(blank=True, null=True, verbose_name="温度")
    e_place = models.FloatField(blank=True, null=True, verbose_name="位置")
    e_pressure = models.FloatField(blank=True, null=True, verbose_name="压力")
    e_remind = models.CharField(blank=True, null=True, max_length=1000, verbose_name="提醒人")
"""
# 报警规则表
class AlarmRule(models.Model):
    pass


# 报警记录表
class AlarmRecord(models.Model):
    pass
"""




