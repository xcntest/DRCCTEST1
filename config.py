import os

root_dir = os.path.dirname(__file__)

evn = '192.168.51.233'

host = evn+":8066/"

#存储图片路径
imagepath = os.path.join(root_dir, "images") #默认用例文件路径
#测试套件路径
casepath = os.path.join(root_dir, "case")
#测试用例请求数据文件夹
datapath = os.path.join(root_dir, "testdata")

#统一身份登录信息
longinfo = {
    "url" :evn+":18020",
    "username": "qaadmin",
    "pwd":"hzmc1234567"
}

#产品库连接信息
proc_mysqldb_info = {
#    'class':'mysql',
    'host': evn,
    'port': 3306,
    'db': 'drcc',
    'user': 'root',
    'password': 'root_drcc',
    'charset' : 'utf8'
}


#添加资产信息
assert_db={
    "sdb_name": "11g主239.120",
    "sdb_user": "system",
    "sdb_pwd": "db_pwd",
    "sip": "192.168.239.120",
    "sos_user": "oracle",
    "sos_pwd": "oracle",
    "tdb_name": "11g主239.120",
    "tdb_user": "system",
    "tdb_pwd": "db_pwd",
    "tip": "192.168.239.120",
    "tos_user": "oracle",
    "tos_pwd": "oracle"
}


#创建资产组字典


groups_dict = {
    'name': '测试模板替换资产组1',
    'desc': '资产组描述1'
}


