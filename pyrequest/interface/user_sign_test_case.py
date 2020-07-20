#encoding=utf-8
import requests,time
import unittest
from db_fixture.test_data import init_data


class UserSignTest(unittest.TestCase):
    """嘉宾签到"""
    def setUp(self):
        self.base_url='http://127.0.0.1:8000/api/user_sign/'

    def test_user_sign_all_null(self):
        """字段为空"""
        data = {'eid':'','phone':''}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10021)
        self.assertEqual(self.result['message'],'参数不能为空')

    def test_user_sign_eid_error(self):
        """eid格式错误"""
        data = {'eid':'wwewe','phone':'12345'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10028)
        self.assertEqual(self.result['message'],'eid格式错误')

    def test_user_sign_eid_null(self):
        """eid为空"""
        data = {'eid':7,'phone':'12345'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10022)
        self.assertEqual(self.result['message'],'发布会不存在')


    def test_user_sign_status_close(self):
        """发布会为关闭状态"""
        data = {'eid':3,'phone':'12345'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10023)
        self.assertEqual(self.result['message'],'发布会为关闭状态，不能签到')


    def test_user_sign_time_start(self):
        """发布会已开始"""
        data = {'eid':4,'phone':'12345'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10024)
        self.assertEqual(self.result['message'],'发布会已开始或已结束')


    def test_user_sign_phone_error(self):
        """手机号为空"""
        data = {'eid':1,'phone':'9876'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10025)
        self.assertEqual(self.result['message'],'手机号为空')

    # 手机号与发布会不匹配
    def test_user_sign_eid_phone_error(self):
        """手机号与发布会不匹配"""
        data = {'eid':1,'phone':'123456'}
        r = requests.post(self.base_url,data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'],10026)
        self.assertEqual(self.result['message'],'此手机号没有参加该发布会')


    # 用户已签到
    def test_user_sign_true(self):
        """用户已签到"""
        data = {'eid': 5, 'phone': '12345'}
        r = requests.post(self.base_url, data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10027)
        self.assertEqual(self.result['message'], '此手机号已经签到')


    def test_user_sign_sucess(self):
        """签到成功"""
        data = {'eid': 1, 'phone': '12345'}
        r = requests.post(self.base_url, data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], '签到成功')



if __name__=='__main__':
    init_data()#初始化接口测试数据
    print('没进去')
    unittest.main()