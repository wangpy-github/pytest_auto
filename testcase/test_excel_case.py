#coding=utf-8
import os
import unittest
from pprint import pprint
import ddt
from HTMLTestRunner.HTMLTestRunner import HTMLTestRunner
from config.Conf import ConfigYaml, get_data_path, get_testcase_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
from common import Base
from common.Base import run_api
from config import Conf
from testcase.test_case_logic.case_logic import logic
import datetime
# 1. 初始化信息，可单独定义或者写成配置文件
case_file = get_data_path() + os.sep + ConfigYaml().get_excel_file()  # 使用绝对路径，相对路径，使用pytest会出错
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file, sheet_name).get_run_data()  # 获取需要运行的测试用例
log = my_log()
data_key = DataConfig
request_params = dict()
# 2. 参数化运行测试用例
@ddt.ddt
class Test_Excel(unittest.TestCase):
    # 初始化参数数据
    @ddt.data(*data_list)
    def test_run(self, case):
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        method = case[data_key.method]
        params = case[data_key.params]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        except_result = case[data_key.except_result]
        r = call_back(case)

        print("请求URL:", request_params.get("url", url))
        print("-------------------------------------------------------------------")
        print("method:", method)
        print("-------------------------------------------------------------------")
        print("headers:", request_params.get("headers", headers))
        print("-------------------------------------------------------------------")
        print("cookies:", request_params.get("cookies", cookies))
        print("-------------------------------------------------------------------")
        print("params:", request_params.get("params", params))
        print("-------------------------------------------------------------------")
        print("响应时间:", r.get("total_seconds", None))
        print("-------------------------------------------------------------------")
        print("期望结果:", r.get("verif_data_pre", except_result))
        print("-------------------------------------------------------------------")
        print("实际结果：")
        pprint(r.get("body", None))

def run(case, res_more=None):
    """
    根据前置接口的返回数据，去获取当前接口的返回数据
    :param case: 当前测试用例
    :param res_more: 当前用例的所有前置接口返回数据   Type：dict
    :return:
    """
    url = ConfigYaml().get_conf_url() + case[data_key.url]
    case_id = case[data_key.case_id]
    method = case[data_key.method]
    params_type = case[data_key.params_type]
    params = case[data_key.params]
    headers = case[data_key.headers]
    cookies = case[data_key.cookies]

    # 根据前置接口的返回数据，去获取当前接口的请求参数
    # 有${}$则处理，无则原数据返回，增加verif_data_pre用于断言使用
    url, headers, cookies, params, verif_data_pre = logic(res_more, case_id=case_id, url=url, headers=headers, cookies=cookies, params=params)
    try:
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        param = Base.json_parse(params)
    except Exception as e:
        log.error("参数格式不对", e)
        raise
    # 组织请求参数为dict，用于之后的allure描述展示
    request_params["url"] = url
    request_params["headers"] = header if header else None
    request_params["cookies"] = cookie if cookie else None
    request_params["params"] = param if param else None

    # 执行当前用例
    r = run_api(url, method, params_type, header, cookie, param)

    # 将需要验证的数据放在响应结果里边，用于之后的断言
    r["verif_data_pre"] = verif_data_pre if verif_data_pre else None
    return r  # 返回最终preA的结果


res_more = dict()
def call_back(case):
    pre_execs = case[data_key.pre_exec]
    if pre_execs:
        for pre_exec in eval(pre_execs):
            pre_case = Data(case_file, sheet_name).get_case_pre(pre_exec)
            res = call_back(pre_case)
            res_more[pre_exec] = res
        return run(case, res_more)
    return run(case, None)

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
        runner = HTMLTestRunner(stream=f, title="自动化接口测试报告", description="描述信息")
        runner.run(suite, verbosity=2)