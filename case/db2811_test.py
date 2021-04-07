# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
import config
        
        
@allure.feature('手动添加资产接口')
class Test2811(object):

    def setup_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetdb/db2811_test.yaml')
        request_obj.ini_case
    
            
    @allure.story('手动添加资产接口')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetdb/db2811_test.yaml',config.assert_db)
    def test_add_assert_db_succeed(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'db2811_test.py', '--alluredir', '../report'])
        
        