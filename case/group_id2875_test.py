# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        
@allure.feature('删除资产组接口测试套件')
class Test2875(object):

    def setup_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertgroups/group_id2875_test.yaml')
        request_obj.ini_case
    
            
    @allure.story('成功删除资产组接口')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertgroups/group_id2875_test.yaml')
    def test_delete_assert_groups_succeed(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'group_id2875_test.py', '--alluredir', '../report'])
        
        