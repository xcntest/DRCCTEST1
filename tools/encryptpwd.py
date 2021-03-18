# -*- coding:utf-8 -*-
'''
@Time       : 2020/9/3 18:44
@Author     : Joy
@FileName   : encryptpwd.py
@description: 将公钥加密成私钥,password 为登录密码
'''
# import base64
# import requests
# import json,warnings
# from Crypto.Cipher import PKCS1_v1_5
# from Crypto.PublicKey import RSA
import hashlib
import config
import os
import jpype


def MD5Encrypt(key):
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    a_md5 = m.hexdigest()
    return a_md5



def AESEncrypt(content):
    # 以下三个路径依次：jvm.dll地址、ApiHelper.jar地址
    jvmPath = jpype.getDefaultJVMPath()
    jarPath = os.path.join(config.root_dir,"lib/AES.jar")


    # startJVM("jvm.dll地址", "-ea", "ApiHelper.jar地址", "ApiHelper.jar依赖库文件夹地址")
    # 第四个参数非必填项，有就填，没有就不填
    #打开JAVA虚拟机
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarPath)

    JDClass = jpype.JClass("com.hzmc.test.AESForNodejs")
    aesHandler = JDClass()
    test = str(aesHandler.encrypt(content))
    #关闭JAVA虚拟
    #jpype.shutdownJVM()

    return test


if __name__ == '__main__':
    a = AESEncrypt("security")
    print(a)

# RSA+base64加密
# def pwd_encryptwd(password='hzmcAdmin'):
#         #忽略异常
#         warnings.filterwarnings('ignore')
#         hostinfo = readfiles.read_yaml('mainhost','interinfo','basic.yaml')
#         host = hostinfo.host
#         url = 'https://' +host+ '/capaa/js/encrypt/encrypt.json'
#         r = requests.get(url=url , verify=False)  # 获取公钥接口
#         publickey = json.loads(r.text)['publicKey']
#         publickey = b'-----BEGIN PUBLIC KEY-----\n' + bytes(publickey, 'utf8') + b'\n' + b'-----END PUBLIC KEY-----'
#         raskey = RSA.importKey(publickey)
#         cipher = PKCS1_v1_5.new(raskey)
#         # cipher_text = base64.b64encode(cipher.encrypt(password))
