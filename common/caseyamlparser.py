# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/28 10:48
@Author     : 测试工程师Jane
@FileName   : caseyamlparser.py
@Description: 处理用例yaml文件
'''

from tools.AttrDict import AttrDict
from common.yamlhandler import HadnlerYaml
from tools.funcreplace import FuncReplace
from common.errors import CaseStoryNotFound,CaseStoryRepeat,CaseParamsError
from common.logs import MyLog
#用于测试,可删除
import config
import os

class CaseYamlParser:
    """ 用例数据解析器 """
    def __init__(self, yaml_path):
        """
        :param yaml_path: yaml_case文件路径
        """
        try:
            self.yaml_data = HadnlerYaml.read_yaml_file(yaml_path)
            self.test_info = AttrDict(self.yaml_data.testinfo)
            self.premise = self.yaml_data.premise    #列表
            self.test_case = self.yaml_data.test_case  #列表
        except Exception as a:
            MyLog.error("用例参数错误{}".format(a))
            raise CaseParamsError


    @property
    def test_suite(self):
        """获取测试套件名称"""
        return self.test_info.case_suite

    @property
    def suite_desc(self):
        """获取套件描述"""
        return self.test_info.descrpiton

    @property
    def case_module_class(self):
        """获取测试用例名称"""
        return self.test_info.module_class

    @property
    def case_set_up(self):
        """获取前置条件方法"""
        return self.yaml_data.set_up

    @property
    def case_tear_down(self):
        """执行后置方法"""
        return self.yaml_data.tear_down

    @property
    def get_all_case(self):
        """获取用例"""
        return self.yaml_data.tear_down


    def get_case_obj_by_name(self,case_data_list,story_name):
        """
        获取用例数据
        :param data: 传入yaml文件内的test_case数据，是个列表
        :param story_name: 传入的测试函数名称
        :return: 返回经过字典属性化的名称与story_name一致的用例数据
        """
        storys = []
        if case_data_list:
            for case in case_data_list:
                case_name = case.get('test_name')
                #从所有用例数据内根据传入的用例名称运行测试用例,此处
                if case_name and case_name == story_name:
                    storys.append(case)
        if len(storys) == 0:
            raise CaseStoryNotFound
        if len(storys) > 1:
            raise CaseStoryRepeat
        return AttrDict(storys[0])



    def _proc_body(self,data):
        #处理有模板替换的body
        if data:
            body = {k: FuncReplace(v).reflex_variable() for k, v in (dict(data)).items()}
        else:
            body = data
        return body



    def proc_data(self,request_data):
        """
        处理request请求数据,
        :request_data: 经过get_case_obj_by_name处理过的数据
        :return: 返加用于request请求的数据
        """
        #处理请求体，替换换要执行函数的内容
        params = self._proc_body(request_data.params)
        data = self._proc_body(request_data.data)
        json = self._proc_body(request_data.json)
        #封装rquest数据
        d = {
            "method": request_data.method.upper(),
            "url": "http://" +config.host+request_data.url,
            "params": params,
            "data": data,
            "json": json,
            "files":request_data.files,
            "headers": request_data.headers,
            "timeout":request_data.timeout,
            "verify": False
        }
        return d


# if __name__ == '__main__':
    # path = os.path.join(config.datapath,"")
    # a = CaseYamlParser(path)
    # data =  a._proc_body(a.test_case[0].get("params"))

