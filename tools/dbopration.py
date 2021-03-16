# -*- coding:utf-8 -*-
'''
@Time       : 2021/3/9 11:01
@Author     : 测试工程师Jane
@FileName   : dbopration.py
@Description:
'''

import pymysql
import config
from common.logs import MyLog


log = MyLog()

def conn_db():
    conninfo = config.proc_mysqldb_info
    try:
        conn = pymysql.connect(**conninfo)
        log.info("数据库连接成功")
        return conn
    except Exception as e:
        log.error("连接失败，失败原因为{}".format(e))



#TODO 优化方法
def quey_db(sql):
    """
    查询数据库
    :param sqlinfo:sql
    :return: 查询元组
    """
    # 判断SQL是否为字段类型查询，如果是，则不带列名，如果不是，则带列名
    conn = conn_db()
    result_list = []
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        with cursor:
            if isinstance(sql,list):
                for subsql in sql:
                    try:
                        cursor.execute(subsql)  # 执行sql
                        result = cursor.fetchall()#获取所有查询结果
                        result_list.append(result[0])
                    except:
                        log.error("未查询到数据，请检查SQL是否正确")
                return result_list
            else:
                try:
                    cursor.execute(sql)  # 执行sql
                    result = cursor.fetchall()  # 获取所有查询结果
                    return result
                except:
                    log.error("未查询到数据，请检查SQL是否正确")
    conn.close()



def join_sql_result(sql):
    """
    接接查询结果
    :param sql: sql list 或者直接是sql
    :return:
    """
    result_list = quey_db(sql)
    result_dict = {}
    for sub_sult in result_list:
        result_dict.update(sub_sult)
    return result_dict






if __name__ == '__main__':
   sqllist = ["select db.id,db.cmdb_id,db.name as db_name,db.db_type,db.instance,db.status as db_status,db.deleted,db.dbversion,h.os_type as os_type,ip,h.status as host_status from db,host as h  where db.id = h.id and h.ip ='192.168.239.120'","select * from account where owner_id ='8'"]
   a = join_sql_result("select * from account where owner_id = '8'")
   b = join_sql_result(sqllist)
   print("b{}".format(b))
   print("a{}".format(a))

