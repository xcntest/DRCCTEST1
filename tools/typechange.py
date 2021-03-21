# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/21 16:02
@Author     : 测试工程师Jane
@FileName   : typechange.py
@Description:
'''



def str2int(value):
    """用于替换返回值"""
    if isinstance(value,str):
        return int(value)
    else:
        return value
