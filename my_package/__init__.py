# -*- coding:utf-8 -*-
'''
@Time       : 2021/1/11 08:00
@Author     : 测试工程师Jane
@FileName   : __init__.py.py
@Description:
'''
from ruamel import yaml
print(yaml.__file__)


## 定义用户yaml tag handler
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

## 注册这个yaml tag handler,此方法用于拼接yaml内的字符
yaml.add_constructor('!join', join)