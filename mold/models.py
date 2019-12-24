from django.db import models
from django.utils import timezone

# Create your models here.
from device.models import DeviceMd
from rbac.models import UserInfo


class Mold(models.Model):
    m_status_choice = (('1', u'生产'), ('2', u'空闲'), ('3', u'维修'), ('4', u'保养'))
    m_num = models.CharField(max_length=100, unique=True, verbose_name="模具编号")
    m_name = models.CharField(max_length=100, blank=True, verbose_name="模具名称")
    m_count = models.CharField(max_length=100, blank=True, verbose_name="模腔数")
    m_life = models.CharField(max_length=100, blank=True, verbose_name="模具寿命")
    m_product = models.CharField(max_length=100, blank=True, verbose_name="生产模数")
    m_status = models.CharField(max_length=100, choices=m_status_choice, verbose_name="模具状态")
    m_user = models.ForeignKey(UserInfo, related_name="mold_adds", verbose_name="维护人员")
    m_created = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "模具"
        verbose_name_plural = "模具"

    def __str__(self):
        return self.m_num

class Repair(models.Model):
    mr_num = models.ForeignKey(to=Mold, related_name="mold", verbose_name="模具编号")
    mr_name = models.CharField(max_length=100, blank=True, verbose_name="模具名称")
    mr_user = models.CharField(max_length=100, blank=True, verbose_name="维修人员")
    mr_start = models.DateTimeField(default=timezone.now, verbose_name="开始时间")
    mr_end = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    mr_appear = models.CharField(max_length=100, blank=True, verbose_name="故障现象")
    mr_method = models.CharField(max_length=100, blank=True, verbose_name="处理方法")
    mr_des = models.CharField(max_length=100, blank=True, verbose_name="备注")




