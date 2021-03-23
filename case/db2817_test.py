# -*- coding:utf-8 -*-
from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        
@allure.feature('获取资产列表接口测试套件')
class Test2817(object):

    def setup_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
        request_obj.ini_case
    
            
    def teardown_class(self):
        request_obj = Send2Reques('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
        request_obj.tear_down_case
            
    @allure.story('资产列表按name查询精确查询')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
    def test_filter_asset_db_by_name(self):
        pass
        
    @allure.story('资产列表按ip查询精确查询')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
    def test_filter_asset_db_by_ip(self):
        pass
        
    @allure.story('资产列表空查询check')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
    def test_filter_asset_db_null(self):
        pass
        
    @allure.story('资产列表总条数check')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/assertdb/db2817_test.yaml')
    def test_filter_asset_db_total(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'db2817_test.py', '--alluredir', '../report'])
        
        