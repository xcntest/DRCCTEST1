# -*- coding:utf-8 -*-
'''
@Time       : 2020/9/3 09:56
@Author     : Joy
@FileName   : getvcode.py
@description :https://www.cnblogs.com/jiahm/p/13539185.html（百度识别图片接口）
'''
#
import requests
import re
import os
import base64
import config
from PIL import Image
from io import BytesIO
from aip import AipOcr
from common.logs import MyLog


class GetVcode:
    def __init__(self,):
        #获取图片接口
        self.url = 'https://'+config.longinfo["url"]+'/sign/imageCode'
        self.headers = {"Content-Type":"application/json;charset=UTF-8"}
        self.session = requests.session()
        self.log = MyLog()
        if os.path.exists(config.imagepath) is False:
            os.makedirs(config.imagepath)
        self.picpath = os.path.join(config.imagepath, 'vcode.png')



    def _write_imge(self,img_base_str):
        # 将图片写入文件
        img= base64.b64decode(img_base_str)  # 得到图片
        file = open(self.picpath, 'wb')
        file.write(img)
        file.close()


    #解码BASE64加密图片
    def get_imageId(self):
         response = self.session.get(url=self.url,verify=False).json()
         image = response.get("data").get("image")
         img_base64 = re.findall(r'data:image/png;base64,(.*)', image)[0]
         self._write_imge(img_base64)
         imageId = response.get("data").get("imageId")
         return imageId


    def _get_new_img(self):
        oriimage = Image.open(self.picpath)
        #对图片转化为灰度图像
        img = oriimage.convert('L')
        img.save(self.picpath)
        i = open(self.picpath, 'rb')
        final_img = i.read()
        return final_img


    #获取验证码
    def get_vcode(self):  # picfile:图片文件名
        # 百度提供
        """ 你的 APPID AK SK """
        # 应用的appid
        APP_ID = '22532565'
        # 应用的appkey
        API_KEY = 'fCvsC8UOdrLFPDGFPpQW0X1I'
        # 应用的secretkey
        SECRET_KEY = 'oMnORbkMcdnTnEm2XNPzls08jOxGEGkx'

        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        """ 调用通用文字识别（高精度版） """
        imageId = self.get_imageId()
        final_img = self._get_new_img()
        message = client.basicAccurate(final_img)
        try:
            vcode = message.get('words_result')[0].get('words')
            return vcode,imageId
        except Exception as e:
            self.log.debug("未获取到有效验证码{}:{}".format(message,e))





if __name__ == '__main__':
   a = GetVcode().get_vcode()
   print(a)



