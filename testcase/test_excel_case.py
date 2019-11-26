import os
from config.Conf import ConfigYaml, get_data_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
import pytest
from utils.AssertUtil import AssertUtil
from common import Base
from common.Base import run_pre, run_api, Correlation
import allure
from config import Conf
from testcase.test_case_logic.case_logic import logic

# 1. 初始化信息，可单独定义或者写成配置文件
case_file = get_data_path() + os.sep + ConfigYaml().get_excel_file()  # 使用绝对路径，相对路径，使用pytest会出错
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file, sheet_name).get_run_data()  # 获取需要运行的测试用例
log = my_log()
data_key = DataConfig
request_params = dict()
# 2. 参数化运行测试用例
class Test_Excel():
    # 初始化参数数据
    @pytest.mark.parametrize("case", data_list)
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

        allure.dynamic.feature(sheet_name)
        allure.dynamic.story(case_model)
        title = "{} {}".format(case_id, case_name)
        allure.dynamic.title(title)
        desc = "<font color='red'>请求URL:</font> {}<Br/>" \
               "<font color='red'>请求类型:</font>{}<Br/>" \
               "<font color='red'>headers:</font>{}<Br/>" \
               "<font color='red'>cookies:</font>{}<Br/>" \
               "<font color='red'>params:</font>{}<Br/>" \
               "<font color='red'>响应时间:</font>{}秒<Br/>" \
               "<font color='red'>期望结果:</font>{}<Br/>" \
               "<font color='red'>实际结果:</font>{}".format(request_params.get("url", url),
                                                         method,
                                                         request_params.get("headers", headers),
                                                         request_params.get("cookies", cookies),
                                                         request_params.get("params", params),
                                                         r.get("total_seconds", None),
                                                         r.get("verif_data_pre", except_result),
                                                         r.get("body", None)
                                                         )
        allure.dynamic.description(desc)

        # AssertUtil().assert_code(r["code"], expected_code=status_code)
        # AssertUtil().assert_in_body(r["body"], expected_body=except_result)


def func(case, res_more):  # ID:preA  res:preB
    url = ConfigYaml().get_conf_url() + case[data_key.url]
    case_id = case[data_key.case_id]
    method = case[data_key.method]
    params_type = case[data_key.params_type]
    params = case[data_key.params]
    headers = case[data_key.headers]
    cookies = case[data_key.cookies]
    # 返回替换后的preD用例数据
    correlation = Correlation()

    # data_：变量名列表 / excel字符串
    data_ = correlation.params_find(url)
    data_variable_list = list()
    if isinstance(data_, list) and len(data_) != 0:
        data_variable_list.extend(data_)

    data_ = correlation.params_find(cookies)
    if isinstance(data_, list) and len(data_) != 0:
        data_variable_list.extend(data_)

    data_ = correlation.params_find(headers)
    if isinstance(data_, list) and len(data_) != 0:
        data_variable_list.extend(data_)

    data_ = correlation.params_find(params)
    if isinstance(data_, list) and len(data_) != 0:
        data_variable_list.extend(data_)
        # 以下填写组合数据的逻辑
        if len(data_variable_list) != 0:
            url, headers, cookies, params, verif_data_pre = logic(res_more, case_id=case_id, url=url, headers=headers, cookies=cookies, params=params)
    try:
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        param = Base.json_parse(params)
    except Exception as e:
        log.error("参数格式不对", e)
        raise
    request_params["url"] = url
    request_params["headers"] = header if header else None
    request_params["cookies"] = cookie if cookie else None
    request_params["params"] = param if param else None
    r = run_api(url, method, params_type, header, cookie, param)  # preD发送请求，获取返回结果
    # 将需要验证的数据放在响应结果里边
    r["verif_data_pre"] = verif_data_pre if verif_data_pre else None
    return r  # 返回最终preA的结果


def call_back(case):
    pre_execs = case[data_key.pre_exec]
    res_more = dict()
    if pre_execs:
        for pre_exec in eval(pre_execs):
            pre_case = Data(case_file, sheet_name).get_case_pre(pre_exec)
            res = call_back(pre_case)
            res_more[pre_exec] = res
        return func(case, res_more)
    return run_pre(case)
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
    report_result_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    # 执行测试用例
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_result_path])
    # 生成测试报告
    Base.allure_report(report_result_path, report_html_path)
