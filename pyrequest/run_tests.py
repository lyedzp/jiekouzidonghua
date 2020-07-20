from db_fixture import test_data
import time
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader

# 指定测试用例为当前文件夹下的interface目录
test_dir = './interface'
testsuit = defaultTestLoader.discover(test_dir,pattern='*_test_case.py')
if __name__=='__main__':
    # 初始化接口数据
    test_data.init_data()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    report_name='./report/'+now+'result.html'
    fp = open(report_name,'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='发布会签到系统接口自动化测试',
                            description='运行环境:MySQL(PyMySql),Requests,unittest')
    runner.run(testsuit)
    fp.close()
