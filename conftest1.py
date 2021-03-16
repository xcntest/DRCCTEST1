# -*- coding:utf-8 -*-
'''
@Time       : 2020/8/31 14:40
@Author     : Joy
@FileName   :
'''

import pytest
import requests
import urllib3
import config
from tools.encryptpwd import MD5Encrypt
from tools.AttrDict import AttrDict
from tools.getvcode import GetVcode
from common.logs import MyLog



@pytest.fixture(scope="session")
def login():
      """登录获取token等信息"""
      #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      log = MyLog()
      req_data = {}
      longinfo = AttrDict(config.longinfo)
      url = 'https://' +longinfo.url+"/sign/login"
      req_data["account"] = '610f73a314e055b4c716058a4cdb09fc'
      req_data["password"] = 'b26941d9e4143513b4c62a1443a78ee7'
      imageCode,imageId = GetVcode().get_vcode()
      headers = {"Conten-Type":"application/json;charset=UTF-8"}
      while True:
            while imageCode is None or len(imageCode)<4:
                  imageCode,imageId = GetVcode().get_vcode()
            else:
                  req_data['imageCode'] = imageCode
                  req_data["imageId"] = imageId
                  response = requests.post(url=url,json=req_data,headers=headers,verify=False)
                  data = response.json()
                  if data["success"]:
                        token = "DRCC "+response.json().get("data").get("token")
                        print(token)
                        return token
                        break
                  else:
                        imageCode, imageId = GetVcode().get_vcode()






if __name__ == '__main__':
    login()






