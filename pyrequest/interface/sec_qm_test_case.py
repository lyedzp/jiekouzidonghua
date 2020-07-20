import requests,unittest
import time,hashlib
class AddEventTest(unittest.TestCase):
    """添加发布会（用户签名+时间戳）"""
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
    def test_sign_null (self):
        """签名为空"""
        datas = {"time":"","sign":""}
        r = requests.post(url=self.base_url,data=datas)
        result = r.json()
        self.assertEqual(result["status"],10012)
        self.assertEqual(result["message"],"user sign null")


    def test_sign_error_get(self):
        """get请求"""
        datas = {"time": "", "sign": ""}
        r = requests.get(url=self.base_url, data=datas)
        result = r.json()
        self.assertEqual(result["status"], 10011)
        self.assertEqual(result["message"], "request error")

    def test_sign_time_out(self):
        """请求时间超时"""
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        #-61秒是为了构造服务端时间-客户端时间超时情况
        self.client_time = str(int(self.client_time)-61)
        print("client time:" + self.client_time)
        datas = {"time": self.client_time, "sign": "sdsdsdssddx"}
        r = requests.post(url=self.base_url, data=datas)
        result = r.json()
        self.assertEqual(result["status"],10013)
        self.assertEqual(result["message"], "user sign timeout")

    def test_sign_sucess(self):
        """时间戳+签名成功,参数为空"""
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]

        md5 = hashlib.md5()
        sign_str = self.client_time + "&Guest-Bugmaster"
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        client_sign = md5.hexdigest()
        datas = {"time":self.client_time,"sign":client_sign}
        s = requests.post(url=self.base_url,data=datas)
        result = s.json()
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'], "必传参数为空")

    def test_sign_sucess(self):
        """时间戳+签名成功,发布会id已存在"""
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]

        md5 = hashlib.md5()
        sign_str = self.client_time + "&Guest-Bugmaster"
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        client_sign = md5.hexdigest()
        datas = {"time":self.client_time,"sign":client_sign,"eid":1}
        s = requests.post(url=self.base_url,data=datas)
        result = s.json()
        self.assertEqual(result['status'],10022)
        self.assertEqual(result['message'], "发布会id已存在")

    def test_sign_sucess(self):
        """签名失败"""
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]

        datas = {"time": self.client_time, "sign": "sdsdsdsds"}
        s = requests.post(url=self.base_url, data=datas)
        result = s.json()
        self.assertEqual(result['status'], 10014)
        self.assertEqual(result['message'], "user sign error")

if __name__=="__main__":
    unittest.main()