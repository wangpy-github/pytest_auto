#coding=utf-8
import os
import pytest
from common import Base
from config import Conf

if __name__ == '__main__':
    # 定义result和html的绝对路径
    report_result_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    # 执行测试用例
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_result_path])
    # 生成测试报告
    Base.allure_report(report_result_path, report_html_path)