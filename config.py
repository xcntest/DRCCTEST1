import os


root_dir = os.path.dirname(__file__)

evn = '192.168.51.***'

host = evn+":8000"

#存储图片路径
imagepath = os.path.join(root_dir, "images") #默认用例文件路径
#统一身份登录信息
longinfo = {
    "url" :"192.168.51.***:***",
    "username": "test2",
    "pwd":"***"
}


#产品库连接信息
proc_mysqldb_info = {
#    'class':'mysql',
    'host': evn,
    'port': 3306,
    'db': 'drcc',
    'user': '***',
    'password': '***',
    'charset' : 'utf8'
}
#用例数据和用例文件路么
casepath = os.path.join(root_dir, "case") #默认用例文件路径
datapath = os.path.join(root_dir, "testdata")

# evn = os.path.join(root_dir, "setting.yaml")
# token = 'Token'






