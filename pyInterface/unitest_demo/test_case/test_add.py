#encoding=utf-8
import unittest
from count import Count
#创建的测试类必须继承unittest.TestCase
class AddTest(unittest.TestCase):
    #每一条用例执行之前都要做的操作可放到setUp
    def setUp(self):
        self.c = Count()
        print("start test")
    #每条用例执行之后的要做的操作放到tearDown
    def tearDown(self):
        print("end test")
    # 测试方法必须以test开头
    def test_add_3_5(self):
        result = self.c.add(3,5)
        # 断言结果是否=8
        self.assertEqual(result,8)
    # 预期结果和实际结果不符，会报failure(失败)
    def test_add_22_33(self):
        result = self.c.add(2.2,3.3)
        self.assertEqual(result,5)
    # 自己代码问题，会报失败，Error
    def test_add_hello(self):
        result = self.c.add()
        self.assertEqual(result, 5)



# 写在if __name__下的代码，只有该文件自己运行时会被执行，其他文件引用该文件，不会执行该文件if __name_下的代码
if __name__ == "__main__":
    # unittest.main(),会一次性执行所有用例，当想单独执行某些用例时不适用
    # unittest.main()
#     测试套件：运行一组测试用例的集合，放到套件里的用例会被执行，未放的不执行
    suit = unittest.TestSuite()
    suit.addTest(AddTest("test_add_3_5"))
    suit.addTest(AddTest("test_add_22_33"))
    #测试运行器：运行测试套件中的用例
    runner = unittest.TextTestRunner()
    runner.run(suit)
