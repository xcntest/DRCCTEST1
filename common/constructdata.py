# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/19 16:06
@Author     : 测试工程师Jane
@FileName   : constructdata.py
@Description:
'''

from tools.funcreplace import FuncReplace
from tools.AttrDict import AttrDict
import config
from common.logs import MyLog

class Constructdata:
    def __init__(self):
        self.logs = MyLog()


    def _proc_body(self,data):
        #处理有模板替换的body
        if data:
            body = {}
            # body = {k: FuncReplace(v).reflex_variable() for k, v in (dict(data)).items()}
            for k,v in (dict(data)).items():
                if isinstance(v,list):
                    v[0] = int(FuncReplace(v[0]).reflex_variable())   #这里是为了处理groupids被模板替换后成了一个字符型
                    body[k] = v
                else:
                    body[k] = FuncReplace(v).reflex_variable()
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
        request_data = AttrDict(request_data)
        try:
            params = self._proc_body(request_data.params)
            data = self._proc_body(request_data.data)
            json = self._proc_body(request_data.json)
        except AttributeError as e:
            self.logs.error("yaml文件内无此参数值，请检查".format(e))
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
