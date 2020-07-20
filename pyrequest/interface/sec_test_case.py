#encoding=utf-8
import unittest
import requests
class GetEventListTest(unittest.TestCase):
    """查询发布会信息（带用户认证）"""
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/sec_get_event_list/'
    def test_get_event_list_auth_null(self):
        """auth为空"""
        r = requests.get(self.url,params={'eid':1})
        self.result = r.json()
        self.assertEqual(self.result['status'],10011)
        self.assertEqual(self.result['message'],'user auth null')
    def test_get_event_list_eid_sucess(self):
        """查询成功"""
        auth_user = ("root", "123456")
        r = requests.get(self.url,auth=auth_user,params={"eid":1})
        self.result = r.json()
        print(self.result)
        self.assertEqual(self.result['status'],200)
        self.assertEqual(self.result['message'],'查询成功')
    def test_get_event_list_suth_error(self):
        """auth错误"""
        auth_user = ("abc","123")
        r = requests.get(self.url,auth=auth_user,params={'eid':1})
        result = r.json()
        print(result)
        self.assertEqual(result['status'],10012)
        self.assertEqual(result['message'],'user auth fail')

    def test_get_event_list_eid_null(self):
        """eid为空"""
        auth_user = ('root', '123456')
        # auth_user = ('liangyuee','123456')
        r = requests.get(self.url,auth=auth_user,params={'eid':''})
        result = r.json()
        print(result)
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'],'参数不能为空')



if __name__=='__main__':
    unittest.main()