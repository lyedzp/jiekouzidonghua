#encoding=utf-8
from pymysql import cursors,connect
from pymysql.err import OperationalError
import os
import configparser as cparser
import pymysql
# 读取db_config.ini文件设置
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\','/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get("mysqlconf","host")
port = cf.get("mysqlconf","port")
db = cf.get("mysqlconf","db_name")
password = cf.get("mysqlconf","password")
user = cf.get("mysqlconf","user")


# 封装mysql基本操作
class DB:
    def __init__(self):
        try:
            self.conn = connect(host=host,
                                port=int(port),
                                db=db,
                                password=password,
                                user=user,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("MySql Error %d:%s"%(e.args[0],e.args[1]))

#         清除表数据
    def clear(self,table_name):
        real_sql="delete from "+table_name+";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()

        #插入表数据
    def insert(self,table_name,table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO "+ table_name + "("+ key +") VALUES("+value+")"
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    def init_data(self,datas):
        for table_name in datas:
            self.clear(table_name)
            for items in datas[table_name]:
                self.insert(table_name,items)
        self.close()


    # 关闭数据库
    def close(self):
        self.conn.close()
if __name__=="__main__":
    # 可以在对应表执行下面这语句：没有传创建时间，默认取当前时间为创建时间
    # alter table guest2_dev.sign_event CHANGE create_time create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    db = DB()
    data1 = {'id':1120,'name':'ssss','status':0,'address':'四川锦江区','start_time':'2019.12.01','`limit`':10}
    data = {'realname': 'lye5', 'phone': '1312456523','email':'56565@qq.com','sign': '0','event_id':'1120'}
    db.clear('sign_guest')
    db.clear('sign_event')
    db.insert('sign_guest',data)
    db.insert('sign_event',data1)
    db.close()


