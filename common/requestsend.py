# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/7 12:08
@Author     : 测试工程师Jane
@FileName   : requestsend.py
@Description:   发送request请求
'''

import requests
import jsonpath
import time
from common.caseyamlparser import CaseYamlParser
from common.yamlhandler import HadnlerYaml
from common.logs import MyLog
from common.login import login
from tools.funcreplace import FuncReplace
import urllib3


class Send2Reques:
    def __init__(self,filepath,case_name):
        """
        :param filepath: 从run_case内传入用例路径
        :param case_name:  单条用例函数名，run_case内的fun_name
        :param login:  从fixture传入的login返回
        """
        self.log = MyLog()
        self.extractinfo = {}   #全局关联参数字典,获取会话内所有接口的关联参数，用于用例模板替换
        self.case_obj = CaseYamlParser(filepath)
        self.case_name = case_name
        self.extractinfo["token"] = "DRCC {}".format(login())


    @property
    def ini_case(self):
        """处理前置接口,获取关联参数"""
        if self.case_obj.premise:
            #如果前置接口有多条，循环取数据，再请求(这里不用return,只写入关联参数)
            for premise_request_data in self.case_obj.premise:
                self.__sendrequest(premise_request_data)

    @property
    def set_up_case(self):
         """前置条件处理，获得内容"""
         if self.case_obj.case_set_up:
            return FuncReplace(self.case_obj.case_set_up).reflex_variable()


    @property
    def tear_down_case(self):
        """前置条件处理，获得内容"""
        if self.tear_down_case:
            return FuncReplace(self.case_obj.case_tear_down).reflex_variable()



    @property
    def run_case(self):
        """处理前置接口,获取关联参数"""
        if self.case_obj.test_case:
            case_request_data = self.case_obj.get_case_obj_by_name(self.case_obj.test_case,self.case_name)#获取测试数据，字典格式
            response = self.__sendrequest(case_request_data)  #获取reponse
            except_dict = case_request_data.expects  #获取期望字典
            return  response,except_dict



    #直接调用的是session接口
    def __sendrequest(self,case_data):
        """

        :param case_data: case数据字典
        :return:
        """
        data = self.case_obj.proc_data(case_data) #获取request_body请求数据
        request_data = HadnlerYaml.replace_yaml_value(data,self.extractinfo)   #使用extract(关联参数字典)替换用例内的参数
        print("请求参数为{}".format(request_data))
        try:

            response = requests.request(**request_data)
            #判断接口status(用于需要跑一会儿的程序)
            if case_data.status:
                status = jsonpath.jsonpath(response.json(),"$.result[0].status")[0]
                while not status == case_data.get('status'):
                    response = requests.request(**request_data)
                    time.sleep(5)
                    status = jsonpath.jsonpath(response.json(), "$.result[0].status")[0]

            # 将下个接口需要的关联参数写入到公共参数字典内
            if case_data.extract:
                for key,value in case_data.get("extract").items():
                    self.extractinfo[key] = jsonpath.jsonpath(response.json(),value)[0]
            else:
                print("该接口无关联参数")
            #TODO 调用assert方法做断言assert_response(response, values.get("validate"))
            return response

        except Exception as e:
            self.log.debug("Exception {} url {}".format(e, request_data["url"]))



# if __name__ == '__main__':
    # request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/DRCC/', "test_get_asset_group")
    # response = request_obj.run_case
    # print(response[0].json())
