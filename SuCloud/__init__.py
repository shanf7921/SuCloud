from __future__ import absolute_import, unicode_literals

# 引入celery实例对象
from .celery import app as celery_app

import pymysql
pymysql.install_as_MySQLdb()