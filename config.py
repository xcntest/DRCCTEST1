import os


root_dir = os.path.dirname(__file__)

evn = '192.168.51.233'

host = evn+":8000"

#存储图片路径
imagepath = os.path.join(root_dir, "images") #默认用例文件路径
#统一身份登录信息
longinfo = {
    "url" :"192.168.51.91:18020",
    "username": "test2",
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
#用例数据和用例文件路么
casepath = os.path.join(root_dir, "case") #默认用例文件路径
datapath = os.path.join(root_dir, "testdata","DRCC")

# evn = os.path.join(root_dir, "setting.yaml")
# token = 'Token'






