# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/27 11:56
@Author     : 测试工程师Jane
@FileName   : createcasefile.py
@Description: 创建用例文档
'''
import os
from common.caseyamlparser import CaseYamlParser
from tools.AttrDict import AttrDict
import config

class CreateCaseFile:
    def __init__(self,case_path=None):
        if not case_path:
            self.case_path = config.casepath
        else:
            self.case_path = case_path

    def create_temp_case_file(self,file_path=None):
        """
        获取路径下的所有yaml数据
        :param file_path:
        :return:
        """
        #如果不传入路径，那就按配置文件的路径处理
        if not file_path:
            file_path = config.datapath
        for root, dirs, files in os.walk(file_path):
            for file in files:
                self.path = os.path.join(root,file)
                print(self.path)
                self.yaml_data = CaseYamlParser(self.path)
                self.__create_single_case_suit()

    # 创建用例文档
    def __create_single_case_suit(self):
            file_name = self.yaml_data.test_suite + '.py'
            case_file_name = os.path.join(self.case_path, file_name) #默认从配置文件取，但传入就显示传入值
            import_ = """from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        """
            #建测试套件
            suit_desc = self.yaml_data.suite_desc
            case_module_class = self.yaml_data.case_module_class
            mod_example = '''
@allure.feature('{}')
class {}(object):
'''.format(suit_desc, case_module_class)
    #
    #         fixture_example ='''
    # request_obj = Send2Reques('{}')
    #
    # @classmethod
    # def setup_class(cls):
    #     cls.request_obj.set_up_case()
    #     cls.request_obj.ini_case()
    #
    # @classmethod
    # def teardow_class(cls):
    #     cls.request_obj.tear_down_case()
    #     '''.format(self.path)
    #
    #         mod_example += fixture_example
            #建测试用例
            for case in self.yaml_data.test_case:
                case_obj =  AttrDict(case)
                case_name = case_obj.test_name
                case_mark = case_obj.mark
                case_desc = case_obj.info
                case_example = '''
    @allure.story('{}')
    @pytest.mark.{}
    @call_case('{}')
    def {}(self):
        pass
        '''.format(case_desc, case_mark,self.path, case_name)
                mod_example += case_example
            import_ += mod_example

            debug_info = ''' 
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', '{}', '--alluredir', '../report'])
        
        '''.format(file_name)

            import_ += debug_info
            with open(case_file_name, 'w', encoding='utf-8') as f:
                f.write(import_)

if __name__ == '__main__':
    CreateCaseFile().create_temp_case_file()