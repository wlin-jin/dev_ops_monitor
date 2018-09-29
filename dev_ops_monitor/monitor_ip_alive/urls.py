#!/usr/bin/env python
# encoding: utf-8
'''
@author: wlin.jin
@contact: wlin.jin@ucloud.cn
@file: urls.py.py
@time: 2018/9/29 9:38
@desc:
'''

from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^monitor_ip/eip_monitor', views.eip_monitor, name="eip_monitor"),
]
