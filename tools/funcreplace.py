# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/7 14:06
@Author     : 测试工程师Jane
@FileName   : funcreplace.py
@Description: 通过字符串模板调用函数，并替换yaml文件内容
'''

import re
from common.errors import KeywordSyntaxError,ReplaceStringIsNone
import importlib
from common.logs import MyLog


class FuncReplace:
    def __init__(self, text):
        self.text = text
        self.logs = MyLog()

    #TODO 后期优化精简代码re模块
    def _get_variable(self):
        """获取${}"""
        list = []
        if self.text:
            fun_str = re.split(";", self.text)   #这里用来分段多个要执行的函数，可能存在字符冲突的情况
            for sub_str in fun_str:
                r = re.findall(r"\$\{(.*)\}$", sub_str, re.I | re.M)
                if r:
                    list.append(r[0])
        if not list:
            self.logs.info("此字符串为正常字符串,替换的字符串为{}".format(self.text))
        return list

    def reflex_variable(self):
        text = self.text
        if isinstance(text, str) is False:
            return text
        # 获取字符串
        text_vars = self._get_variable()   #拿到的是个列表或者空字符
        if text_vars:
            for var in text_vars:
                s_text = var.split('|')
                if len(s_text) > 1:
                    arg_find = re.findall(r"\((.*)\)$", ''.join(s_text[: -1]), re.I | re.M)  #判断是否有多个调数调用，若有，报错
                    if len(arg_find) > 1:
                        raise KeywordSyntaxError
                    try:
                        # 执行函数
                        mod = importlib.import_module(s_text[-1])   #取得函数，函数名
                        func_text = "{}.{}".format("mod", s_text[0])
                        value = eval(func_text)   #运行函数，得到返回值
                        text = value
                        # sub_str = '${%s}' % var
                        # text = str(text).replace(sub_str, str(value))   #返回值替换掉模板内容，要注意返回值格式的问题
                    except ModuleNotFoundError:
                        raise KeywordSyntaxError
        return text


if __name__ == '__main__':
    sqllist = [
        "select db.id,db.cmdb_id,db.name as db_name,db.db_type,db.instance,db.status as db_status,db.deleted,db.dbversion,h.os_type as os_type,ip,h.status as host_status from db,host as h  where db.id = h.id and h.ip ='192.168.239.120'",
        "select * from account where owner_id ='8'"]

    str1 = """${join_sql_result(%s)|tools.dbopration}""" % sqllist
    str2 = """${quey_db("select h.ip from host as h ")|tools.dbopration}"""
    str3 = ""
    str4 = 1000
    str5 = "奇怪的数字"
    result = FuncReplace(sqllist).reflex_variable()
    print(result)
    # import json
    # nos = json.loads(result)
    # print(nos)
    # for i in a._get_variable():
    #     print(i)