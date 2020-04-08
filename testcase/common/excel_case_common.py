# coding=utf-8
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

"""
递归：https://www.cnblogs.com/yizhipanghu/p/10717161.html
return的本质是停止距离它最近的函数
"""

from common.ExcelData import Data
from common.ExcelConfig import DataConfig
from utils.AssertUtil import AssertUtil
import allure

data_key = DataConfig
request_params = dict()
res_more = dict()


# 参数化运行测试用例
class Base_Excel_Test():
    env_url = None
    env_excel_sheet = None
    case_file = None

    def test_run(self, case):
        url = self.env_url + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        method = case[data_key.method]
        params = case[data_key.params]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        except_result = case[data_key.except_result]
        r = self.call_back(case)

        allure.dynamic.feature(self.env_excel_sheet)
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
               "<font color='red'>实际结果:</font>{}".format(
            request_params.get("url", url),
            method,
            request_params.get("headers") if request_params.get("headers") else headers,
            request_params.get("cookies") if request_params.get("cookies") else cookies,
            request_params.get("params") if request_params.get("params") else params,
            r.get("total_seconds", None),
            r.get("verif_data_pre") if r.get("verif_data_pre") else except_result,
            r.get("body", None))
        allure.dynamic.description(desc)

        # 增加响应结果断言
        if r.get("verif_data_pre"):
            for verif_data_pre in r.get("verif_data_pre"):
                AssertUtil().assert_in_body(str(r["body"]), expected_body=verif_data_pre)  # TODO 添加str，已经dumps
        if except_result:
            AssertUtil().assert_in_body(str(r["body"]), expected_body=except_result)

    def call_back(self, case):
        pre_execs = case[data_key.pre_exec]
        if pre_execs:
            for pre_exec in eval(pre_execs):
                pre_case = Data(self.case_file, self.env_excel_sheet).get_case_pre(pre_exec)
                res = self.call_back(pre_case)
                res_more[pre_exec] = res
            return self.run(case, res_more)
        return self.run(case, None)

    def run(self, case, res_more=None):
        """
        根据前置接口的返回数据，去获取当前接口的返回数据
        :param case: 当前测试用例
        :param res_more: 当前用例的所有前置接口返回数据   Type：dict
        :return:
        """
        pass


if __name__ == '__main__':
    Base_Excel_Test()
