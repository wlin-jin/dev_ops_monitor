#!/usr/bin/env python
# encoding: utf-8
'''
@author: wlin.jin
@contact: wlin.jin@ucloud.cn
@file: Common.py
@time: 2018/9/29 10:53
@desc:
'''


class Common(object):
    def __init__(self):
        pass

    @classmethod
    def return_data(cls, code='success', message='', data={}):
        '''
        返回统一格式结果
        '''

        ret = {}
        ret['code'] = code
        ret['message'] = message
        ret['data'] = data

        return ret
