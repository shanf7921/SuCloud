# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-12-23 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0005_auto_20191223_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paramtime',
            name='t_error',
            field=models.BooleanField(default=False),
        ),
    ]
