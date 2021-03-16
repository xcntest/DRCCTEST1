from common.callcase import call_case
import allure
import pytest
from common.requestsend import Send2Reques 
        
        
@allure.feature('查询资产接口')
class Test111(object):

    @allure.story('全量查询资产')
    @pytest.mark.smoking
    @call_case('/Users/xiongting/Desktop/工作/DRCC/DRCCTEST/testdata/DRCC/dbtest_11.yaml')
    def test_get_asset_group(self):
        pass
         
        
if __name__ == '__main__':
    pytest.main(['-s', '-q', '-v', 'dbtest_11.py', '--alluredir', '../report'])
        
        