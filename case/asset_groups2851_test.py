# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
import config
        
        
@allure.feature('创建资产组信息接口测试套件')
class Test2851(object):

    @allure.story('创建资产组信息接口')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assetgroups/asset_groups2851_test.yaml',config.groups_dict)
    def test_add_assert_group(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'asset_groups2851_test.py', '--alluredir', '../report'])
        
        