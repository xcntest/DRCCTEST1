# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/28 15:42
@Author     : 测试工程师Jane
@FileName   : callcase.py
@Description:
'''


import os
from common.errors import  CaseFileNotFound
from common.requestsend import Send2Reques
from common.assertactions import AssertActions
from common.logs import MyLog


def call_case(file_path=None):
    def middle(func):
        def wrapper(*args, **kwargs):
            func_name = getattr(func, '__name__')#获取用例函数名称
            #判断yaml文件路径是否存在
            if os.path.exists(file_path) is False:
                raise CaseFileNotFound
            request_obj = Send2Reques(file_path,func_name)
            response,except_dict = request_obj.run_case   #执行用例,获得resopnse
            if except_dict:
                AssertActions(except_dict, response).exec_assert()   #断言
            return func(*args, **kwargs)
        return wrapper
    return middle


