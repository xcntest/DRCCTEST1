# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/25 19:21
@Author     : 测试工程师Jane
@FileName   : AttrDict.py
@Description:
'''

#字典属性化访问,获取字典内的信息时
class AttrDict:
    def __init__(self,d:dict):
        self.__dict__.update(d if isinstance(d,dict) else {})

    def __setattr__(self, key, value):
        #允许修改属性
        raise NotImplementedError

    def __repr__(self):
        print(self.__dict__)
        return "<AttrDict {}> ".format(self.__dict__)


    def __len__(self):
        return len(self.__dict__)




if __name__ == '__main__':
    d = {'mysql':{'host':'192.168.51.126'}}
    a = AttrDict(d['mysql'])
    print(type(a))
