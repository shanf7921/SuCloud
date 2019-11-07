# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-05 19:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceMd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_type', models.CharField(choices=[('1', '注塑机'), ('2', '辅机')], max_length=100)),
                ('d_num', models.CharField(max_length=100, unique=True)),
                ('d_brank', models.CharField(blank=True, max_length=100)),
                ('d_model', models.CharField(blank=True, max_length=100)),
                ('d_name', models.CharField(blank=True, max_length=100)),
                ('d_status', models.CharField(choices=[('1', '运行'), ('2', '待机'), ('3', '离线')], max_length=100)),
                ('d_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('d_photo', models.ImageField(blank=True, upload_to='image/%Y/%m/%d')),
                ('d_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_adds', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
