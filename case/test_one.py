# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/16 17:27
@Author     : 测试工程师Jane
@FileName   : testone.py
@Description:
'''

def test_m1_1():
    print('这是 subpath1/test_module1.py::test_m1_1')
    assert 1==1

def test_m1_2():
    print('这是 subpath1/test_module1.py::test_m1_2')
    assert 2==2

def test_spec_1():
    print ('这是 subpath1/test_module1.py::test_spec_1')
    assert 2 == 2
