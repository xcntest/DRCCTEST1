# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/25 19:17
@Author     : 测试工程师Jane
@FileName   : yamlhandler.py
@Description:  处理yaml的方法集
'''

import os
from tools import AttrDict
from ruamel import yaml
from common.errors import YamlFormatError
from string import Template
import json


class HadnlerYaml:

    @classmethod
    def read_yaml_file(cls, yaml_path=None):
        """
        读取yaml
        :param yaml_path: yaml文件的路径
        :return: 转为python格式的yaml数据
        """
        with open(yaml_path, encoding='utf-8') as cf:
            try:
                data = yaml.load(cf,Loader=yaml.Loader)
                print(data)
                yaml_dada = AttrDict.AttrDict(data)  #交读取的yaml字内属性化
                return yaml_dada
            except yaml.scanner.ScannerError:
                raise YamlFormatError


    #替换用例内的数据
    @classmethod
    def replace_yaml_value(cls,yamldata,extractinfo):
        """
        :param yamldata:  用例数据
        :param extractinfo: 替换内容的字典，写在的request的fixture文件内
        :return: 返回替换后的内容
        """
        #yamldata是字典是转换为json后替换
        yaml_test = Template(json.dumps(yamldata)).safe_substitute(extractinfo)
        case_data = yaml.safe_load(yaml_test)
        return case_data

#
# if __name__ == '__main__':
#       # a = "/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/DRCC/"
#       # HadnlerYaml.read_yaml_file(a)