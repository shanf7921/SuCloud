# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-12-23 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0004_auto_20191223_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paramtime',
            name='t_error',
            field=models.NullBooleanField(default=False),
        ),
    ]
