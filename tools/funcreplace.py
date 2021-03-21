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


    def _get_variable(self):
        r = re.findall(r"\$\{(.*)\}$", self.text, re.I | re.M)
        if len(r) == 1:
            return r

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
    sql = '${str2int(79)|tools.typechange}'
    result = FuncReplace(sql).reflex_variable()
    print(result)
    # import json
    # nos = json.loads(result)
    # print(nos)
    # for i in a._get_variable():
    #     print(i)