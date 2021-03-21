# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        
@allure.feature('创建资产组信息接口')
class Test2851(object):

    def teardown_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertgroups/asset_groups2851_test.yaml')
        request_obj.tear_down_case
            
    @allure.story('创建资产组信息接口')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertgroups/asset_groups2851_test.yaml')
    def test_add_assert_group(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'asset_groups2851_test.py', '--alluredir', '../report'])
        
        