#coding=utf-8
import os
import pytest
from common import Base
from common.Base import zip_new_report
from config import Conf
import datetime

if __name__ == '__main__':
    # 定义result和html的绝对路径
    current_time = datetime.datetime.now().strftime("%A-%Y-%m-%d#%H-%M-%S")
    report_result_path = Conf.get_report_path() + os.sep + "result" + os.sep + current_time
    report_html_path = Conf.get_report_path() + os.sep + "html" + os.sep + current_time
    # 执行测试用例
    pytest.main(["-s", "./testcase/test_case_module_login/test_feed_login.py", "--alluredir", report_result_path])
    # 生成测试报告
    Base.allure_report(report_result_path, report_html_path)
    # 打包测试报告
    new_zip_report_path = zip_new_report()