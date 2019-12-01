#coding=utf-8
import os
import unittest
from HTMLTestRunner.HTMLTestRunner import HTMLTestRunner
from config import Conf
import datetime
from config.Conf import get_testcase_path

if __name__ == '__main__':
    # unittest.main()

    # 创建一个测试套件，并向其中加载测试用例
    # suite = unittest.TestLoader().loadTestsFromTestCase(Test_Excel)
    # 显式运行测试没并且通过设置verbosity设定对每一个测试方法产生测试结果
    # unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.defaultTestLoader.discover(get_testcase_path(), "test*.py")
    # 报告文件存放路径
    current_time = datetime.datetime.now().strftime("%A-%Y-%m-%d#%H-%M-%S")
    report_html_path = Conf.get_report_path() + os.sep + current_time + ".html"

    with open(report_html_path, "wb") as f:
        # 实例化HTMLTestRunner对象，传入报告文件流f
        runner = HTMLTestRunner(stream=f, title="自动化接口测试报告", description="执行人：wpy")
        runner.run(suite, verbosity=2)