# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        
@allure.feature('手动添加资产接口')
class Test2811(object):

    @allure.story('手动添加资产接口')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2811_test.yaml')
    def test_add_assert_db(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'db2811_test.py', '--alluredir', '../report'])
        
        