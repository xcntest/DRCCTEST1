# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
import config
        
        
@allure.feature('删除资产接口测试套件')
class Test2815(object):

    def setup_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetdb/asset_id2815_test.yaml')
        request_obj.ini_case
    
            
    def teardown_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetdb/asset_id2815_test.yaml')
        request_obj.tear_down_case
            
    @allure.story('无容灾对无切换编排删除资产')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetdb/asset_id2815_test.yaml',config.assert_db)
    def test_assert_deleted_succeed(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'asset_id2815_test.py', '--alluredir', '../report'])
        
        