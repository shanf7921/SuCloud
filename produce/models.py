from django.db import models

# Create your models here.
from django.utils import timezone

from device.models import DeviceMd


class Order(models.Model):
    o_status_choice = (('1', u'未开始'), ('2', u'暂停中'), ('3', u'生产中'), ('4', u'已完成'), ('5', u'未分配'))
    o_id = models.CharField(max_length=32, verbose_name="订单号")
    o_name = models.CharField(max_length=32, verbose_name="产品名称")
    o_customer = models.CharField(max_length=32, verbose_name="客户")
    o_count = models.IntegerField(verbose_name="产品数量")
    o_finish = models.IntegerField(default=0, verbose_name="生产数量")
    o_start = models.CharField(max_length=32, verbose_name="开始时间")
    o_end = models.CharField(max_length=32, verbose_name="结束时间")
    o_day = models.IntegerField(verbose_name="所需天数")
    o_create = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    o_status = models.CharField(max_length=32, default=1, choices=o_status_choice, verbose_name="订单状态")
    o_des = models.CharField(max_length=32, verbose_name="备注")

class OrderDevice(models.Model):
    o_k = models.ForeignKey(to=Order, related_name="od_order")
    d_k = models.ForeignKey(to=DeviceMd, related_name="od_device", blank=True)
    o_id = models.IntegerField(verbose_name="订单ID")
    d_id = models.IntegerField(verbose_name="机台ID")
    od_count = models.IntegerField(default=0, verbose_name="生产数量")
    od_active = models.BooleanField(default=True)
    od_created = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    od_taskid = models.CharField(max_length=200,blank=True)

