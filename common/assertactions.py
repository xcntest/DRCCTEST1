# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/28 15:57
@Author     : 测试工程师Jane
@FileName   : assertactions.py
@Description:
'''
import json
import re
import pytest
import allure
from common.errors import ResponseNotJson,CaseAssertNotSport,CaseAssertFailed
from common.logs import MyLog
from tools.funcreplace import FuncReplace




class AssertActions(object):
    """断言处理器"""
    def __init__(self, except_dict, response):
        self.asserts_dict = except_dict
        self.response = response
        self.assert_type = ['body', 'headers', 'http_code']
        self.log = MyLog()

    def assert_parse(self):
        pass

    def body_assert_parse(self, key):
        """
        拿到断言字典的key，取response相应的值
        :param key:
        :return:  response字典
        """
        body_rule = key.split('.')
        body_data = self._format_response_body()
        if len(body_rule) == 1:    #如果不取body的子值，直接返回整个body
            return body_data
        try:
            json.dumps(body_data)    #将返回值转为dict，如果无法转，报错
        except (ValueError, TypeError):
            raise ResponseNotJson

        for rule in body_rule[1:]:
            section = re.findall(r"\[(.*)\]$", rule, re.I | re.M)   #取索引下标[0]等
            if len(section) == 0:    #如果没有索引，直接返回respones["result"]
                body_data = body_data[rule]
            elif len(section) == 1:      #如果有，再按"[",切分，取response["result"],然后再返回 result[0]
                rule_new = rule.split('[')[0]
                body_data = body_data[rule_new]
                try:
                    s = int(section[0])
                    body_data = body_data[s]
                except ValueError:
                    raise CaseAssertNotSport
        return body_data

    def headers_assert_parse(self, key):
        headers_rule = key.split('.')
        if len(headers_rule) == 2:
            return self._format_response_headers()[headers_rule[-1]]
        else:
            raise CaseAssertNotSport

    def http_code_assert_parse(self, key):
        key_rule = key.split('.')
        if len(key_rule) == 1 and key_rule[0] == 'http_code':
            return self.response.status_code
        else:
            raise CaseAssertNotSport

    def exec_assert(self):
        for k, v in self.asserts_dict.items():
            self.log.debug('断言对象:{}'.format(k))
            mod = k.split('.')[0]
            if mod not in self.assert_type:
                raise CaseAssertNotSport
            if mod == 'body':
                k_str = self.body_assert_parse(k)

                with allure.step("response body校验"):
                    allure.attach("实际值为", str(k_str))
            elif mod == 'headers':
                k_str = self.headers_assert_parse(k)

                with allure.step("response head校验"):
                    allure.attach("实际值为", str(k_str))
            elif mod == 'http_code':
                k_str = self.http_code_assert_parse(k)

                with allure.step("response http_code校验"):
                    allure.attach("实际值为", str(k_str))
            self.log.debug('断言对象取值:{}'.format(k_str))
            v_str = FuncReplace(v).reflex_variable()
            self.log.debug('期望取值:{}'.format(v_str))
            if isinstance(v_str,dict):
                self._compare_dict_assert(v_str,k_str)
            else:
                try:
                    pytest.assume(k_str == v_str)
                except AssertionError:
                    raise CaseAssertFailed('断言失败:实际值{} != 期望值{}'.format(k_str, v_str))

    def _format_response_body(self):
        try:
            content = self.response.json()
        except (TypeError, ValueError):
            content = self.response.content.decode("utf-8")
        return content

    def _format_response_headers(self):
        return self.response.headers


    def _compare_dict_assert(self,except_dict,response_dict):
        """
        如果断言和返回都是字典，比较字典内所有的值
        :param except_dict:
        :param response_dict:
        :return:
        """

        for k,v in except_dict.items():
            k_list = set(response_dict.keys())
            if k in k_list:
                try:
                    self.log.debug("resopnse boby单个断言值为：{},期望值为：{}".format(k,response_dict.ge(k)))
                    pytest.assume(v == response_dict.get(k))
                    with allure.step("response body单个值校校验"):
                        allure.attach("实际值为", str(response_dict.get(k)))
                except AssertionError:
                    raise CaseAssertFailed('断言失败:实际值{} != 期望值{}'.format(response_dict.get(k),v))




# if __name__ == '__main__':
    # from common.requestsend import Send2Reques
    # sqllist =  ["select db.id,db.cmdb_id,db.name as db_name,db.db_type,db.instance,db.status as db_status,db.deleted,db.dbversion,h.os_type as os_type,ip,h.status as host_status from db,host as h  where db.id = h.id and h.ip ='192.168.239.120'","select * from account where owner_id ='8'"]
    # request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/DRCC/', "test_get_asset_group")
    # response, except_dict = request_obj.run_case
    # dict_key = {"body.result[0]":"join_sql_result(%s)|common.dbopration" % sqllist}
    # key = "body.result[0]"
    # a = AssertActions(dict_key,response)
    # body_data = a.body_assert_parse(key)
    # print(body_data)
