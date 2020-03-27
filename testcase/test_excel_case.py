#coding=utf-8
"""
https://www.cnblogs.com/fengf233/p/11799619.html#autoid-5-0-0
unittest使用：
核心：
    1. TestCase
    2. TestSuite 测试套件：多条测试用例集合在一起执行，就是一个TestSuite
    3. TestRunner 是一个用于执行和输出测试结果的组件
    4. TestLoader
    5. Fixture

import  unittest
class Test_XX(unittest.TestCase):
    def test_xxx(self, case):
        print("abc")
    def test_XXX(self, case):
        print("bcd")

管理用例：
    方式1. 通过addTest()的方式
        # 1. 实例化测试套件
        suite = unittest.TestSuite()
        # 2. 添加用例到套件，ClassName：为类名；MethodName：为方法名  --> suite.addTest(ClassName("MethodName"))
        suite.addTest(Test_XX("test_xxx"))
        suite.addTest(Test_XX("test_XXX"))
        # 3. 实例化TextTestRunner，并执行测试套件
        runner  =  unittest.TextTestRunner()
        runner.run(suite)

    方式2. 通过TestLoader()方式组织TestSuite，此用法可以同时测试多个类
        test_loader = unittest.TestLoader()
        suite1 = test_loader.loadTestsFromTestCase(ClassName1)
        suite2 = test_loader.loadTestsFromTestCase(ClassName2)
        suite = unittest.TestSuite([suite1, suite2])
        unittest.TextTestRunner().run(suite)

    方式3. 统一管理测试用例执行，可以管理某一个文件下的测试用例
        discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py',top_level_dir=None)
            注意：discover()方法中的start_dir只能加载当前目录下的.py文件，如果加载子目录下的.py文件，需在每个子目录下放一个_init_.py文件。
            start_dir：要测试的模块名或测试用例目录路径
            pattern='test*.py'：表示用例文件名的匹配原则
            top_level_dir=None：测试模块的顶层目录，如果没有顶层目录，默认为None
        使用：
            discover_suite = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')
            runner = unittest.TextTestRunner()
            runner.run(discover_suite)


跳过用例和预期失败
    unittest.skip(reason):无条件的跳过装饰的测试，说明跳过测试的原因
    unittest.skipIf(condition,reason)：跳过装饰的测试，如果条件为真。
    unittest.skipUnless(condition,reason):跳过装饰的测试，除非条件为真。
    unittest.expectedFailure():测试标记为失败，不管执行结果是否失败，统一标记为失败，但不会抛出错误信息。


执行顺序
    unittest框架默认根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z,a-z。所以上文测试方法test_isupper()会比test_upper()先执行
    同理测试类以及测试文件也是按照这个顺序执行，但如果你使用addTest()的方式添加了测试，会按照添加的顺序执行


HTMLTestRunner输出测试报告
    python2时期的产物，现在python3需要修改其内容才能用
    使用：
        testsuite = unittest.TestSuite()
        testsuite.addTest(ClassName("MethodName"))
        fp = open('./result.html', 'wb')
        runner = HTMLTestRunner(stream=fp, title='测试报告', description='测试执行情况')
        runner.run(testsuite)
        fp.close()


命令行运行：
    #运行测试文件
    python -m unittest test_module
    #测试单个测试类
    python -m unittest test_module.test_class
    #测试多个测试类
    python -m unittest test_module.test_class test_module2.test_class2
    #通配符匹配测试文件执行
    python -m unittest -p test*.py
    #显示详细信息
    python -m unittest -v test_module
    #帮助
    python -m unittest -h
"""
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