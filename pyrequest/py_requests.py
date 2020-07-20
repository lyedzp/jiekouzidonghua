#encoding=utf-8
import requests
import unittest
class GetEvevtList(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'
    def test_get_event_list(self):
        r = requests.get(self.url,params={'eid':1})
        result = r.json()
        self.assertEqual(result['message'],"查询成功")
        self.assertEqual(result['status'],200)

    def test_get_event_null(self):
#         发布会id为空
        r = requests.get(self.url,params={'eid':''})
        result = r.json()
        self.assertIn(result['message'],'参数不能为空')
# class Testmy():
#     def teston(self):
#         print('你是猪')
if __name__=='__main__':
    unittest.main()
    # suit = unittest.TestSuite()
    # suit.addTest(GetEvevtList("test_get_event_list"))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)