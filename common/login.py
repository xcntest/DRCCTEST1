# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/14 10:27
@Author     : 测试工程师Jane
@FileName   : login.py
@Description:
'''


import requests
import config
from tools.encryptpwd import MD5Encrypt
from tools.AttrDict import AttrDict
from tools.getvcode import GetVcode
from common.logs import MyLog
from tools.encryptpwd import AESEncrypt


def login():
      """登录获取token等信息"""
      #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      log = MyLog()
      req_data = {}
      loginfo = AttrDict(config.longinfo)
      url = 'https://' +loginfo.url
      req_data["account"] = AESEncrypt(loginfo.username)
      req_data["password"] = AESEncrypt(loginfo.pwd)
      import jpype
      if not jpype.isJVMStarted():
            jpype.shutdownJVM()
      imageCode,imageId = GetVcode().get_vcode()
      headers = {"Conten-Type":"application/json;charset=UTF-8"}
      while True:
            while imageCode is None or len(imageCode)<4:
                  imageCode,imageId = GetVcode().get_vcode()
            else:
                  req_data['imageCode'] = imageCode
                  req_data["imageId"] = imageId
                  response = requests.post(url=url+"/sign/login",json=req_data,headers=headers,verify=False)
                  data = response.json()
                  if data["success"]:
                        token = response.json().get("data").get("token")
                        print(token)
                        return token
                        break
                  else:
                        imageCode, imageId = GetVcode().get_vcode()


if __name__ == '__main__':
    login()
