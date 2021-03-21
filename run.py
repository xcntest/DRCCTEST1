# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/14 16:33
@Author     : 测试工程师Jane
@FileName   : run.py
@Description:
'''

import pytest
import os
from tools.createcasefile import CreateCaseFile




if __name__ == '__main__':
    CreateCaseFile().create_temp_case_file()
    # pytest.main(['-s', '-q', '--alluredir', './result/'])
    # os.system("allure generate ./result/ -o ./allure-report/ --clean")
    # os.system("allure open -h 127.0.0.1 -p 8883 ./allure-report/")


