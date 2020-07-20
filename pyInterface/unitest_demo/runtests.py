#encoding=utf-8
import unittest
# 要执行某个文件夹下的测试文件，第一个参数传文件夹相对路径
#第二个参数传要执行的测试文件的规则，测试文件都是以test_开头，所以会执行test_case文件夹下以test开头的文件
#并把以test开头的文件中以test开头的方法都添加到测试套件中
suit = unittest.defaultTestLoader.discover(
    start_dir='./test_case',
    pattern='test*.py')

if __name__=="__main__":
    run = unittest.TextTestRunner()
    run.run(suit)