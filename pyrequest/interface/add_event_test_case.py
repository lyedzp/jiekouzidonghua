# encoding=utf-8
import unittest
import requests
from db_fixture import test_data
from parameterized import parameterized


class AddEventTest(unittest.TestCase):
    """添加发布会"""
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/add_event/'

    # def tearDown(self):
    #     pass
    #
    #
    # def test_add_event_all_null(self):
    #     """添加发布会字段为空"""
    #     data = {'eid': '', 'name': '', 'limit': '', 'status': '', 'address': '', 'start_time': ''}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10021)
    #     self.assertEqual(self.result['message'], '必传参数为空')
    #
    # def test_add_event_id_exits(self):
    #     """发布会id已存在"""
    #     data = {'eid': 2, 'name': '锤子发布会12', 'limit': '10', 'status': 1, 'address': '四川成都',
    #             'start_time': '2019-09-09 12:00:23', 'create_time': '2019-09-09 12:00:23'}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10022)
    #     self.assertEqual(self.result['message'], '发布会id已存在')
    #
    # def test_add_event_name_exists(self):
    #     """发布会名称重复"""
    #     data = {'eid': 15, 'name': '红米pro发布会', 'limit': '10', 'status': 1, 'address': '四川成都',
    #             'start_time': '2019-09-09 12:00:23'}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10023)
    #     self.assertEqual(self.result['message'], '发布会名称重复')
    #
    # def test_add_event_data_type_error(self):
    #     """数据类型错误"""
    #     data = {'eid': 18, 'name': '魅族发布会70', 'limit': '10', 'status': 1, 'address': '四川成都',
    #             'start_time': '2019-09-'}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10024)
    #     self.assertEqual(self.result['message'], '发布会时间格式错误，It must be YYYY-MM-DD HH:MM:SS')
    #
    # def test_add_event_success(self):
    #     """发布会添加成功"""
    #     data = {'eid': 6, 'name': '魅族发布会77', 'limit': '10', 'status': 1, 'address': '四川成都',
    #             'start_time': '2019-09-09 12:00:23'}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 200)
    #     self.assertEqual(self.result['message'], '发布会新增成功')
    #
    # def test_add_event_eid_error(self):
    #     """发布会id格式错误"""
    #     data = {'eid': 'ww', 'name': '魅族发布会78', 'limit': '10', 'status': 1, 'address': '四川成都',
    #             'start_time': '2019-09-09 12:00:23'}
    #     r = requests.post(self.base_url, data=data)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10025)
    #     self.assertEqual(self.result['message'], 'eid格式错误')


    # 以下是数据驱动测试，测试方法就写一个，靠不同数据构建不同测试用例，一条数据就是一条用例，否则要向上面一样一个用例一个方法
    @parameterized.expand([
        # 第一个参数是用例名称，代表这是测试为空的用例
        """必传参数为空"""
        ('null','','','','','','',10021,'必传参数为空'),
        # ('id_exits','2','锤子发布会12','10',1,'四川成都','2019-09-09 12:00:23',10022,'发布会id已存在'),
        ('name_exists', '15', '红米pro发布会', '10', 1, '四川成都', '2019-09-09 12:00:23', 10023, '发布会名称重复'),
        ('data_type_error', '18', '魅族发布会70', '10', 1, '四川成都', '2019', 10024, '发布会时间格式错误，It must be YYYY-MM-DD HH:MM:SS'),
        ('eid_error', 'ww', '魅族发布会78', '10', 1, '四川成都', '2019-09-09 12:00:23', 10025,
         'eid格式错误'),
        ('success', '6', '魅族发布会77', '10', 1, '四川成都', '2019-09-09 12:00:23', 200,
         '发布会新增成功')
    ])
    def test_add_event(self,casename,eid,name,limit,status,address,start_time,statuscode,message):
        data = {'eid': eid, 'name': name, 'limit': limit, 'status': status, 'address': address, 'start_time': start_time}
        r = requests.post(self.base_url, data=data)
        self.result = r.json()
        self.assertEqual(self.result['status'], statuscode)
        self.assertEqual(self.result['message'], message)


if __name__=='__main__':
    test_data.init_data()
    unittest.main()
