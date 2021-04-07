# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/7 12:08
@Author     : 测试工程师Jane
@FileName   : requestsend.py
@Description:   发送request请求
'''

import requests
import jsonpath
from common.constructdata import Constructdata
from common.caseyamlparser import CaseYamlParser
from common.yamlhandler import HadnlerYaml
from common.logs import MyLog
from common.login import login
from tools.funcreplace import FuncReplace

#定义全局变量
extractinfo = {}
extractinfo["token"] = "DRCC {}".format(login())
log = MyLog()

#直接调用的是session接口
def sendrequest(case_data,setupdata=None):
    """

    :param case_data: case数据字典
    :return:
    """
    #处理如果请求要先查询库获取值的，传入值
    if setupdata:
        for k,v in setupdata.items():
            extractinfo[k] = v
    log.debug("替换模板的字典为{}".format(extractinfo))
    case_data_replace = HadnlerYaml.replace_yaml_value(case_data,extractinfo)
    request_data = Constructdata().proc_data(case_data_replace) #获取request_body请求数据
#        request_data = HadnlerYaml.replace_yaml_value(data,self.extractinfo)   #使用extract(关联参数字典)替换用例内的参数
    log.debug("请求参数为{}".format(request_data))
    try:

        response = requests.request(**request_data)
        # #判断接口status(用于需要跑一会儿的程序)
        # if case_data.status:
        #     status = jsonpath.jsonpath(response.json(),"$.result[0].status")[0]
        #     while not status == case_data.get('status'):
        #         response = requests.request(**request_data)
        #         time.sleep(5)
        #         status = jsonpath.jsonpath(response.json(), "$.result[0].status")[0]
        #
        # 将下个接口需要的关联参数写入到公共参数字典内
        if case_data.get("extract"):
            for key,value in case_data.get("extract").items():
                extractinfo[key] = jsonpath.jsonpath(response.json(),value)[0]  #获取到的关联参数变为INT类型，这里可能导致一至错误
                log.info("所取得的关联参数为{}".format(extractinfo[key]))
        else:
            log.info("该接口无关联参数")
        return response
    except Exception as e:
        log.debug("接口调用失败,错误为{}，请求地址为：{}".format(e, request_data["url"]))




class Send2Reques:
    def __init__(self,filepath,case_name=None,rep_dict=None):
        """
        :param filepath: 从run_case内传入用例路径
        :param case_name:  单条用例函数名，run_case内的fun_name
        :param login:  从fixture传入的login返回
        """
        #全局关联参数字典,获取会话内所有接口的关联参数，用于用例模板替换
        self.case_obj = CaseYamlParser(filepath,rep_dict)
        self.case_name = case_name


    @property
    def ini_case(self):
        """处理前置接口,获取关联参数"""
        if self.case_obj.get_premise:
            log.info("开始执行前置条件接口")
            #如果前置接口有多条，循环取数据，传入的是个列表
            for premise_request_data in self.case_obj.get_premise:
                try:
                    sendrequest(premise_request_data)
                except Exception as e:
                    log.error("前置接口调用失败，失败url{}".format(premise_request_data["url"]))
        else:
            log.info("无前置接口")


    @property
    def set_up_case(self):
         """前置条件处理，获得内容"""
         if self.case_obj.case_set_up:
            return FuncReplace(self.case_obj.case_set_up).reflex_variable()


    @property
    def tear_down_case(self):
        """前置条件处理，获得内容"""
        log.info("开始执行后置回收数据操作")
        if self.case_obj.case_tear_down:
            for teardown_request_data in self.case_obj.case_tear_down:
                try:
                    sendrequest(teardown_request_data)
                except Exception as e:
                    log.error("后置接口调用失败,请求url{}".format(teardown_request_data["url"]))
        else:
            log.info("无后置接口处理")



    @property
    def run_case(self):
        """处理前置接口,获取关联参数"""
        if self.case_obj.get_all_case:
            case_request_data = self.case_obj.get_case_obj_by_name(self.case_obj.get_all_case,self.case_name)#获取测试数据，字典格式
            response = sendrequest(case_request_data,self.set_up_case)  #获取reponse
            except_dict = case_request_data["expects"]  #获取期望字典
            return  response,except_dict


    # def sendrequest(case_data):
    #     """
    #
    #     :param case_data: case数据字典
    #     :return:
    #     """
    #     self.log.debug("传入case值参数为{}".format(case_data))
    #     self.log.debug("替换模板的字典为{}".format(self.extractinfo))
    #     case_data = HadnlerYaml.replace_yaml_value(case_data, self.extractinfo)
    #     request_data = self.case_obj.proc_data(case_data)  # 获取request_body请求数据
    #     #        request_data = HadnlerYaml.replace_yaml_value(data,self.extractinfo)   #使用extract(关联参数字典)替换用例内的参数
    #     self.log.debug("请求参数为{}".format(request_data))
    #     try:
    #
    #         response = requests.request(**request_data)
    #         # #判断接口status(用于需要跑一会儿的程序)
    #         # if case_data.status:
    #         #     status = jsonpath.jsonpath(response.json(),"$.result[0].status")[0]
    #         #     while not status == case_data.get('status'):
    #         #         response = requests.request(**request_data)
    #         #         time.sleep(5)
    #         #         status = jsonpath.jsonpath(response.json(), "$.result[0].status")[0]
    #         #
    #         # 将下个接口需要的关联参数写入到公共参数字典内
    #         if case_data.get("extract"):
    #             for key, value in case_data.get("extract").items():
    #                 self.log.info("取得的关联值为：")
    #                 self.extractinfo[key] = jsonpath.jsonpath(response.json(), value)[0]
    #                 self.log.info("所取得的关联参数为{}".format(self.extractinfo[key]))
    #         else:
    #             self.log.info("该接口无关联参数")
    #         return response
    #     except Exception as e:
    #         self.log.debug("接口调用失败,错误为{}，请求地址为：{}".format(e, request_data["url"]))

if __name__ == '__main__':
    request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetgroups/asset_groups2851_test.yaml','test_add_assert_group')
    response, except_dict = request_obj.run_case
    print(response.status_code)


