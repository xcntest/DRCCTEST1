# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/15 16:01
@Author     : 测试工程师Jane
@FileName   : getyapi.py
@Description:  获取yapi有更新的接口，生成临时接口用例文档
'''
import requests
from common import logs
import time
import os
from ruamel import yaml
import json

class GetYapi(object):

    def __init__(self,userapi, passwdapi, group_id):
        self.logs = logs.MyLog()
        self.data = {'email': userapi,
                     'password': passwdapi}
        self.pwd = passwdapi
        self.group_id = group_id
        self.session = requests.session()
        self.apiurl = "http://192.168.238.242:3000"
        #self.path_data_lists = []  # 接口数据(list)
        self.pathdicts = {}  #存取单个从yaml内抓去的数据
        self.count = 0   #统计接口总数
        self.filecount = 0  #统计yaml总数
        self.root_dir = os.path.dirname(os.path.abspath("."))
        self.yaml_dir = ""  #写入yaml的路径
        self.pathid = ""   #用于写入总文件内的ID
        self.total_file = os.path.join(self.root_dir,"total_iface_info.yaml")
        self.id_list = set()
        self.total_data = {}  #存总的接口数据
        #读取总接口信息文件,用于判断新增接口
        with open(self.total_file,encoding='utf-8') as cf:
            data = yaml.load(cf, Loader=yaml.Loader)
            if data:
                for key in data.keys():
                      self.id_list.add(key)
        loginheader = {'Content-Type': 'application/json;charset=utf-8'}
        #登录
        res = self.session.post(url=self.apiurl + "/api/user/login", json=self.data,verify=False, headers=loginheader)
        self.logs.info("登录yapi结果：{}".format(res.json().get("errmsg")))
        #登录后爬取yaml数据


    def create_yaml_by_yapi(self):
        self.__get_mode_id()


    def __get_mode_id(self):
        """
        获取path信息 根据产品id(group_id) 获取对应的模块id
        """
        getid = {'group_id': self.group_id, 'page': '1', 'limit': '500000'}
        res = self.session.get(url=self.apiurl + "/api/project/list", verify=False, params=getid)
        #获取模块列表
        ids = res.json().get("data").get("list")
        for i in range(len(ids)):
            self.pathmodlename = ids[i].get("name")
            if self.pathmodlename == "DRCC":
                # 根据模块名称创建yaml文件夹层
                self.yaml_dir = os.path.join(self.root_dir,"update",self.pathmodlename)
                if os.path.exists(self.yaml_dir) is False:
                    os.makedirs(self.yaml_dir)
                self.basepath = ids[i].get("basepath")    #获取基地址，用于路径拼接
                self.__get_pathid_by_mouled_id(ids[i].get("_id"))  #获取模块ID，并调用处理接口的方法


    def __get_pathid_by_mouled_id(self, _id):
        """通过模块id找寻path—id
        :param _id: 模块id
        """
        res = self.session.get(self.apiurl + "/api/interface/list?page=1&limit=9999&project_id=%s" % _id,verify=False)
        ids = res.json().get("data").get("list")
        #获取单个接口信息的ID
        for i in range(len(ids)):
            self.pathid = ids[i].get("_id")
            self.logs.info("接口ID为{}".format(self.pathid))
            self.__get_pathdata_by_pathid(self.pathid)


    def __get_pathdata_by_pathid(self, pathid):
        """根据pathid获取每个接口的详细信息

        :param pathid: 接口id
        """
        #将数据写入caseyaml
        data_dict = {}
        res = self.session.get(url=self.apiurl + "/api/interface/get?id=%s" % pathid, verify=False).json()
        pathdata = res.get("data")
        data_dict["modle_name"] = self.pathmodlename  # 接口所属模块名称
        #拼接case_suite
        name = pathdata.get("query_path").get("path").split('/')
        case_suite = name[-1].lstrip(':')+str(self.pathid)+"_"+"test"
        #处理要写入yaml的数据
        data_dict["case_suite"] = case_suite  #yaml文件名
        data_dict["descrption"] = pathdata.get("title")  # 接口名称
        data_dict["module_class"] = "Test"+ str(self.pathid) # 接口名称case_suite.replace("_",'')+
        data_dict["url"] = self.basepath + pathdata.get("path")  # 接口地址
        data_dict["method"] = pathdata.get("method")  # 接口请求方法
        if pathdata.get("req_headers"):
            data_dict["headers"] = pathdata.get("req_headers")[0].get("value")  #获取请求头Content-Type
        params_data = {}  # 请求表单的表单数据
        if pathdata.get("req_query"):
            for requestdatas in pathdata.get("req_query"):
                params_data[requestdatas.get("name")] = ""
        data_dict['params'] = params_data
        key_value_dict = {}  # 请求表单的表单数据
        #判断是否有数据再取值
        if pathdata.get("req_body_other"):
            json_data = json.loads(pathdata.get("req_body_other"))
            self.logs.info("获取出来的json参数为{}".format(json_data))
            if json_data.get("properties"):
                for k,v in json_data.get("properties").items():
                    key_value_dict[k] = "" #取requestdata的key和备注，在写入yaml时还需要再处理
        data_dict["json"] = key_value_dict  #后去请请json内容
        data_dict["up_中time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(int(pathdata.get("up_time"))))  # 接口变更时间
        data_dict["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime(int(pathdata.get("add_time"))))  # 接口添加时间
        data_dict["path_creat_user"] = pathdata.get("username")  # 接口创建者
        self.pathdicts = data_dict
        # 将数据写入totalyaml
        if self.pathid not in self.id_list or self.id_list is None:
            #创建总用例文件
            self.__create_total_file()
            #创建yaml用例文件
            self.__create_yaml_file()

        #self.path_data_lists.append(data_dict)  # 追加每个接口的数据信息到列表中
        self.count += 1
        self.logs.info(("第{}个接口{}的数据已经抓取完毕").format(self.count, data_dict["url"]))   #打印日志


    def __create_total_file(self):
        """创建总接口信息文件，用于过滤已经成生过文件的接口"""
        self.total_data = {}
        self.total_data[self.pathid] = self.pathdicts.get("descrption")
        with open(self.total_file, 'a', encoding='utf-8') as s:
            content = yaml.dump(self.total_data, Dumper=yaml.RoundTripDumper,allow_unicode=True)
            s.write(content)


    def __create_yaml_file(self):
        """创建yaml文件"""
        #存yaml列表
        self.logs.info("接口获取的数据为{}".format(self.pathdicts))
        yaml_data = {}   #整个文档
        testinfo = {}   #存入test_info
        testinfo["case_suite"] = self.pathdicts.get("case_suite")
        testinfo["descrpiton"] = self.pathdicts.get("descrption")
        testinfo["module_class"] = self.pathdicts.get("module_class")
        yaml_data["testinfo"] = testinfo

        yaml_data["premise"] = ""
        yaml_data["set_up"] = ""
        yaml_data["tear_down"] = ""
        #加入case文件
        case_list = []
        case_data = {}
        case_data["test_name"] =""
        case_data["info"] = self.pathdicts.get("descrption")
        case_data["mark"] = ""
        case_data["method"] = self.pathdicts.get("method")
        case_data["url"] = self.pathdicts.get("url")
        case_data["headers"] = {"Authorization":'$token'}
        case_data["timeout"] = 8
        case_data["params"] = self.pathdicts.get("params")
        case_data["data"] = ""
        case_data["files"] = ""
        case_data["json"] = self.pathdicts.get("json")
        case_data["status"] = ""
        case_data["extract"] = ""
        case_data["expects"] = ""
        case_list.append(case_data)
        #加入case
        yaml_data["test_case"] = case_list

        # 装写入的配置文件写入到yaml
        yaml_file_name = self.pathdicts.get("case_suite")+".yaml"
        yaml_data_file = os.path.join(self.yaml_dir,yaml_file_name)
        self.filecount += 1
        self.logs.info("创建第{}个文件".format(self.filecount))
        with open(yaml_data_file, 'w', encoding='utf-8') as s:
            content = yaml.dump(yaml_data, Dumper=yaml.RoundTripDumper,allow_unicode=True)
            s.write(content)



if __name__ == '__main__':
    data =  GetYapi(userapi="xiongting@hzmc.com.cn", passwdapi="24totoro-", group_id="12")
    data.create_yaml_by_yapi()








