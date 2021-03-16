# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/15 11:01
@Author     : 测试工程师Jane
@FileName   : checkjurisdiction.py
@Description: 还未经过调试
'''
import requests
import json
import time


class CheckUrlJurisdiction(object):
    """
    实例初始化字段说明
    userapi: api后台登录账号
    useradmin: base后台登录账号
    passwdapi: api后台登录密码
    passwdadmin: base后台登录密码
    group_id: api后台需要检测产品id(base:35    团购:176)
    self.countTotal: path总数
    self.countnum: path权限不足数量
    self.pathmodle: path所属模块名称
    self.pathname: path详细名称
    self.time: 运行花费时间
    """

    def __init__(self, userapi, useradmin, passwdapi, passwdadmin, group_id):
        self.userapi = userapi
        self.useradmin = useradmin
        self.passwdapi = passwdapi
        self.passwdadmin = passwdadmin
        self.group_id = group_id
        self.countTotal = 0
        self.countnum = 0
        self.pathmodle = ""
        self.pathname = ""
        self.time = float()
        #登录url
        self.apiurl = "http://abcxcc.imwork.net:3000"
        self.adminurl = "http://base.host.com"
        self.api = requests.session()
        self.admin = requests.session()
        """api_login"""
        loginjson = {'email': self.userapi,
                     'password': self.passwdapi}
        loginheader = {'Content-Type': 'application/json;charset=UTF-8'}
        print("api后台登录状态:", self.api.post(url=self.apiurl + "/api/user/login", data=json.dumps(loginjson), verify=False,
                                          headers=loginheader).json().get("errmsg"))
        """admin_login"""
        loginbody = {'name': useradmin, 'password': passwdadmin, 'verify_code': ''}
        print("base后台登录状态: %s" % self.admin.post(url=self.adminurl + "/superAdmin/loginSuper/login", data=loginbody,
                                                 verify=False).json().get("status"))

    def geturlpath(self):
        """根据group_id获取对应模块id limit为每页模块条数"""
        print("正在检测发布系统遗漏的接口地址(本次程序检测所花费时间可能较长，请耐心等待)")
        starttime = time.clock()
        getid = {'group_id': self.group_id, 'page': '1', 'limit': '50'}
        ids = self.api.get(url=self.apiurl + "/api/project/list", verify=False, params=getid).json().get("data").get(
            "list")
        for i in range(0, len(ids)):
            self.pathmodle = ids[i].get("name")
            self.get_path_by_id(ids[i].get("_id"))
        timeend = time.clock()
        self.time = str("%.2f" % (timeend - starttime))

    """通过模块id找寻path"""

    def get_path_by_id(self, _id):
        """避免翻页，条数设置为999"""
        details = self.api.get(self.apiurl + "/api/interface/list?page=1&limit=999&project_id=%s" % _id,
                               verify=False).json()
        for j in range(0, len(details.get("data").get("list"))):
            self.countTotal += 1
            path = details.get("data").get("list")[j].get("path")
            self.pathname = details.get("data").get("list")[j].get("title")
            self.check_path(path)

    """根据path提取出没有权限的信息"""

    def check_path(self, path):

        """检查是否有权限"""
        result = self.admin.get(url=self.adminurl + path, verify=False)
        if result.status_code == 200:
            try:
                if result.content.decode("utf-8").find("权限") != -1:
                    print("%s  url信息:%s/%s" %
                          (path, self.pathmodle, self.pathname))
                    self.countnum += 1
            except UnicodeDecodeError:
                pass


if __name__ == "__main__":
    path = CheckUrlJurisdiction("apiuser", "baseuser", "apipasswd", "basepasswd", "12")
    path.geturlpath()
    print("总共检测path数 %s" % path.countTotal)
    print("权限不足path数 %s" % path.countnum)
    print("本次检测所需时间为 %s秒" % path.time)