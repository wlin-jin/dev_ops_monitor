# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from service.MonitorEip import MonitorEip

# Create your views here.


def eip_monitor(request):
    ip_list = request.GET.get('ips')
    if not ip_list:
        return JsonResponse({'data': 'params is null', 'code': 1})
    ip_list = ip_list.split(',')
    # ip_list = ['106.75.124.104', '106.75.124.104', '106.75.124.104']
    ret = MonitorEip().batch_ping(ip_list=ip_list)
    return JsonResponse({'data': ret, 'code': 0})