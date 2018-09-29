#!/usr/bin/env python
# encoding: utf-8
'''
@author: wlin.jin
@contact: wlin.jin@ucloud.cn
@file: MonitorEip.py
@time: 2018/9/29 9:51
@desc:
'''
import subprocess
import re
import socket
import cStringIO
import traceback
import logging
import copy_reg
import types
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
logger = logging.getLogger('django')


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


class MonitorEip(object):

    def check_ping(self, eip, size=1472):
        cmd = "ping -s {0} -c 5 -w 3 -i 0.2 {1}".format(size, eip)
        logger.info(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        loss = 0
        while True:
            line = p.stdout.readline()
            logger.info(line)
            print line
            if not line:
                break
            result = re.search(r"\s(\d+)\%\spacket\sloss", line)
            if not result:
                continue
            loss = int(result.groups()[0])
        if loss == 100:
            logger.error(loss)
            return {'ip': eip, 'stat': 1}
        return {'ip': eip, 'stat': 0}

    def check_tcp(self, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(10)
        try:
            conn.connect((host, int(port)))
            logger.info("connect success")
            conn.close()
        except socket.timeout:
            logger.error("socket timeout")
            return {'ip': host, 'port': port, 'stat': 2}
        except:
            logger.error("socket exception")
            return {'ip': host, 'port': port, 'stat': 3}
        return {'ip': host, 'port': port, 'stat': 0}

    def batch_ping(self, batch=10, ip_list=[]):
        if not ip_list:
            logger.error('iplist is null')
            return {'code': 'fail', 'msg': 'iplist is null', 'data': ''}
        logger.info('start batch ping')
        data = []
        with futures.ProcessPoolExecutor(max_workers=int(batch)) as e:
            ret = e.map(self.check_ping, ip_list)
            data.extend(ret)
        logger.info('end batch ping')
        return data

    def batch_checktcp(self, batch=10, ip_list=[]):
        if not ip_list:
            logger.error('iplist is null')
            return {'code': 'fail', 'msg': 'iplist is null', 'data': ''}
        logger.info('start batch ping')
        data = []
        with futures.ProcessPoolExecutor(max_workers=int(batch)) as e:
            ret = e.map(self.check_tcp, ip_list)
            data.extend(ret)
        logger.info('end batch ping')