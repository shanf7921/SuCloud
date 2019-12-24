from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Menu(models.Model):
    """菜单"""
    title = models.CharField(max_length=32, verbose_name='菜单')
    icon = models.CharField(max_length=32, verbose_name='图标', blank=True)

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = "菜单"

    def __str__(self):
        return self.title

class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=128, verbose_name='含正则的url')

    menu = models.ForeignKey(to='Menu', verbose_name='菜单', null=True, blank=True, help_text='null表示非菜单')

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):
        return self.title

class Role(models.Model):
    """角色表"""
    title = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='拥有的权限', blank=True)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """用户表"""
    user = models.ForeignKey(User, related_name='u_info')
    uname= models.CharField(max_length=32, verbose_name='姓名', blank=True)
    email = models.EmailField(max_length=64, verbose_name='邮箱', blank=True)
    phone = models.CharField(max_length=64, verbose_name='手机', blank=True)
    roles = models.ManyToManyField(to='Role', verbose_name='拥有的角色', blank=True)
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
    def __str__(self):
        return 'user {}'.format(self.user.username)

