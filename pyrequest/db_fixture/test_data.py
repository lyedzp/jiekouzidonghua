#encoding=utf-8
import sys
# sys.path.append('../db_fixture')
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB
#     构造测试数据
datas={
    'sign_event':[
        {'id':1,'name':'红米pro发布会','`limit`':10,'status':'1','start_time':'2019-12-30 13:00:12','address':'四川成都'},
        {'id':2,'name':'可参加人数为0','`limit`':0,'status':'1','start_time':'2019-12-01 13:00:12','address':'四川成都'},
        {'id':3,'name':'当前状态为0关闭','`limit`':10,'status':'0','start_time':'2019-12-01 13:00:12','address':'四川成都'},
        {'id':4,'name':'发布会已结束','`limit`':10,'status':'1','start_time':'2019-12-01 13:00:12','address':'四川成都'},
        {'id':5,'name':'小米5发布会','`limit`':10,'status':'1','start_time':'2019-12-30 13:00:12','address':'四川成都'},
    ],
    'sign_guest':[
        {'realname':'lye1','phone':'12345','email':'123@qq.com','sign':0,'event_id':1},
        {'realname':'has sign','phone':'12345','email':'123@qq.com','sign':1,'event_id':5},
        {'realname':'lye3','phone':'123456','email':'123@qq.com','sign':0,'event_id':5}
    ]
}

def init_data():
    DB().init_data(datas)
    print('121212121212121212121212121212121343434343434')

# if __name__=='__main__':
#     init_data()