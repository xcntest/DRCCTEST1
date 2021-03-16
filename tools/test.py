
#操作关系型数据库，除PG外，PG使用psycopg2
from sqlalchemy import create_engine
#操作redis数据库
from string import Template
import config


class MySQLCil(object):
    """利用sqlalchemy进行数据库操作"""
    def __init__(self,  sql):
        self.sql = sql
        database = config.proc_mysqldb_info
        chart_set = database.get('charset')
        if database['class'] == 'mysql':
            self.pool = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                database['user'],
                database['password'],
                database['host'],
                database['port'],
                database['db'],
            )
            if chart_set:
                self.pool = self.pool + '?' + 'charset={}'.format(chart_set)
        self.engine = create_engine(self.pool)

    def _run(self):
        result = self.engine.execute(self.sql)
        try:
            data = result.fetchall()
            print(data)
            return data
        except Exception as e:
            return None


    @property
    def result(self):
        return self._run()



def mysql_select(sql):
    """mysql查询"""
    return MySQLCil(sql).result


if __name__ == '__main__':
    mysql_select("select id from asset_group")
