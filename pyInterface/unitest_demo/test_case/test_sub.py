#encoding=utf-8
import unittest
from count import Count
class subTest(unittest.TestCase):
    def setUp(self):
        self.c = Count()
        print("start test")


    def tearDown(self):
        print("end test")


    def test_sub_3_5(self):
        result = self.c.sub(3, 5)
        self.assertEqual(result, -2)

    def test_sub_5_3(self):
        result = self.c.sub(5, 3)
        self.assertEqual(result, 2)
if __name__ == "__main__":
    # unittest.main(),会一次性执行所有用例，当想单独执行某些用例时不适用
    # unittest.main()
#     测试套件：运行一组测试用例的集合，放到套件里的用例会被执行，未放的不执行
    suit = unittest.TestSuite()
    suit.addTest(subTest("test_sub_5_3"))
    #测试运行器：运行测试套件中的用例
    runner = unittest.TextTestRunner()
    runner.run(suit)
