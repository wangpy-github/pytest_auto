#coding=utf-8
"""
安装pytest：pip3 install -U pytest
检查版本：pytest --version

执行方式：
    命令行执行： pytest -s test_sample.py
    主函数执行：pytest.main(["-s", "test_sample.py"])
    pytest参数：
        -s 表示支持控制台打印，如果不加，print 不会出现任何内容
        -q 安静模式，不打印信息
函数级别方法： setup 和 teardown
类级别方法： setup_class 和 teardown_class

插件：
    测试报告插件： pip3 install pytest-html
    失败重试插件：pip3 install pytest-rerunfailures

配置文件pytest.ini：
    addopts = -s --html=report/report.html --reruns 3
    addopts = -s 当前目录下的scripts文件夹 -可自定义
    testpaths = testcase 当前目录下的scripts文件夹下，以test_开头，以.py结尾的所有文件 -可自定义
    python_files = test_*.py  当前目录下的scripts文件夹下，以test_开头，以.py结尾的所有文件中，以Test_开头的类 -可自定义
    python_classes = Test_*  当前目录下的scripts文件夹下，以test_开头，以.py结尾的所有文件中，以Test_开头的类内
    python_functions = test_*  以test_开头的方法 -可自定义

pytest数据参数化：
    一个参数使用：
        @pytest.mark.parametrize("name", ["xiaoming", "xiaohong"])
    多个参数使用：
        @pytest.mark.parametrize(("username", "password"), [("zhangsan","zhangsan123"),("xiaoming", "xiaoming123")])
        @pytest.mark.parametrize("username,password", [("zhangsan","zhangsan123"),("xiaoming", "xiaoming123")])

pytest断言：
    assert xx 判断xx为真
    assert not xx 判断xx不为真
    assert a in b 判断b包含a
    assert a == b 判断a等于b
    assert a != b 判断a不等于b

Allure：
    安装：
        安装python插件  pip3 install allure-pytest
        安装allure : 前置条件已部署java环境
    # 添加行参数
        addopts = -s --alluredir ./report/result  使用allure生成测试结果
    生成HTML命令：
        allure generate report/result -o report/html --clean
"""

import os
from config.Conf import ConfigYaml, get_data_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
import pytest
from utils.AssertUtil import AssertUtil
from common import Base
import allure
from config import Conf
from testcase.test_case_module_login.case_logic import logic
import datetime
from common.Base import run_api, zip_new_report

"""
测试环境信息
"""
# 1. 初始化信息，可单独定义或者写成配置文件
conf = ConfigYaml()
env_url = conf.get_conf_url("dev")
env_excel_file = conf.get_excel_file("dev")
env_excel_sheet = conf.get_excel_sheet("dev")
case_file = get_data_path() + os.sep + env_excel_file  # 使用绝对路径，相对路径使用pytest会出错

# 获取需要运行的测试用例数据
data_list = Data(case_file, env_excel_sheet).get_run_data()
log = my_log()
data_key = DataConfig
request_params = dict()
# 2. 参数化运行测试用例
class Test_Excel():
    # 初始化参数数据
    # @pytest.mark.timeout(0.03)  # 当前用例限定0.03s超时
    # @pytest.mark.flaky(reruns=3, reruns_delay=1)  # 如果失败则延迟1s后重跑
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        url = env_url + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        method = case[data_key.method]
        params = case[data_key.params]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        except_result = case[data_key.except_result]
        r = call_back(case)

        allure.dynamic.feature(env_excel_sheet)
        allure.dynamic.story(case_model)
        title = "{} {}".format(case_id, case_name)
        allure.dynamic.title(title)
        desc = "<font color='red'>请求URL:</font> {}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>请求类型:</font>{}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>headers:</font>{}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>cookies:</font>{}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>params:</font>{}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>响应时间:</font>{}秒<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>期望结果:</font>{}<Br/>" \
               "<hr style='height:1px;border:none;border-top:1px dotted #185598;'/> " \
               "<font color='red'>实际结果:</font>{}".format(request_params.get("url", url),
                                                         method,
                                                         request_params.get("headers") if request_params.get("headers") else headers,
                                                         request_params.get("cookies") if request_params.get("cookies") else cookies,
                                                         request_params.get("params") if request_params.get("params") else params,
                                                         r.get("total_seconds", None),
                                                         r.get("verif_data_pre") if r.get("verif_data_pre") else except_result,
                                                         r.get("body", None)
                                                         )
        allure.dynamic.description(desc)

        # 增加响应结果断言
        if r.get("verif_data_pre"):
            for verif_data_pre in r.get("verif_data_pre"):
                AssertUtil().assert_in_body(str(r["body"]), expected_body=verif_data_pre)   # TODO 添加str，已经dumps
        if except_result:
            AssertUtil().assert_in_body(str(r["body"]), expected_body=except_result)

def run(case, res_more=None):
    """
    根据前置接口的返回数据，去获取当前接口的返回数据
    :param case: 当前测试用例
    :param res_more: 当前用例的所有前置接口返回数据   Type：dict
    :return:
    """
    url = env_url + case[data_key.url]
    case_id = case[data_key.case_id]
    method = case[data_key.method]
    params_type = case[data_key.params_type]
    # 公共变量被替换后的字符串数据
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
            pre_case = Data(case_file, env_excel_sheet).get_case_pre(pre_exec)
            res = call_back(pre_case)
            res_more[pre_exec] = res
        return run(case, res_more)
    return run(case, None)
"""
递归：https://www.cnblogs.com/yizhipanghu/p/10717161.html
用例ID             前置条件
goods_detail       无
checkOrder         goods_detail
checkOrder         creat_cart
done               checkOrder
return的本质是停止距离它最近的函数
"""

if __name__ == '__main__':
    # 定义result和html的绝对路径
    current_time = datetime.datetime.now().strftime("%A-%Y-%m-%d#%H-%M-%S")
    report_result_path = Conf.get_report_path() + os.sep + "result" + os.sep + current_time
    report_html_path = Conf.get_report_path() + os.sep + "html" + os.sep + current_time
    # 执行测试用例
    pytest.main(["-s", "test_excel_case_login.py", "--alluredir", report_result_path])
    # 生成测试报告
    Base.allure_report(report_result_path, report_html_path)
    # 打包测试报告
    new_zip_report_path = zip_new_report()
