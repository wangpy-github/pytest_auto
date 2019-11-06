import os
from config.Conf import ConfigYaml, get_data_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
from utils.RequestsUtil import Request
import json
import pytest
from utils.AssertUtil import AssertUtil
from common import Base

"""
测试用例excel参数化
步骤：
1. 初始化信息
    1. 初始化测试用例文件
    2. 测试用例sheet名称
    3. 获取需要运行的测试用例数据
    4. log日志
2. 测试用例方法，参数化运行
    1. 初始化信息，url/data/headers/json
    2. 接口请求
    

动态关联步骤：
1、验证前置条件
2、有前置条件，则找到执行前置用例
3、发送请求，获取前置用例结果
4、替换Headers变量
    1、验证请求中是否${}$，返回${}$内容
    2、根据内容token，查询 前置条件测试用例返回结果token = 值
    3、根据变量结果内容，替换
5、请求发送
    1、查询，公共方法
    2、替换，公共方法
    3、验证请求中是否${}$，返回${}$内容，公共方法
    4、关联方法
"""
# 1. 初始化信息，可单独定义或者写成配置文件
# case_file = os.path.join("../data", ConfigYaml().get_excel_file())    # 相对路径，使用pytest会出错
case_file = get_data_path() + os.sep + ConfigYaml().get_excel_file()    # 使用绝对路径
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file,sheet_name).get_run_data()                 # 获取需要运行的测试用例
log = my_log()
data_key = DataConfig

def run_api(url, method, params_type, header=None, cookie=None, params=None):
    """
    发送api请求
    """
    request = Request()
    if len(str(params).strip()) is not 0:
        params = json.loads(params)
    if str(method).lower() == "get":
        r = request.get(url, headers=header, cookies=cookie)
    elif str(method).lower() == "post":
        if str(params_type).lower() == "form_data":
            r = request.post(url, data=params, headers=header, cookies=cookie)
        elif str(params_type).lower() == "json":
            r = request.post(url, json=params, headers=header, cookies=cookie)
    else:
        log.error("错误请求methods：", method)
    return r


def run_pre(pre_case):
    """
    执行前置测试用例
    """
    # 初始化前置条件测试用例的参数
    url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
    method = pre_case[data_key.method]
    params = pre_case[data_key.params]
    params_type = pre_case[data_key.params_type]
    headers = pre_case[data_key.headers]
    cookies = pre_case[data_key.cookies]
    # 判断headers和cookies是否存在
    header = Base.json_parse(headers)
    cookie = Base.json_parse(cookies)
    r = run_api(url,method=method,params_type=params_type, header=header, cookie=cookie, params=params)
    return r

def get_correlation(headers,cookies,pre_res):
    #验证是否有关联
    headers_para,cookies_para = Base.params_find(headers,cookies)
    #有关联，执行前置用例，获取结果
    if len(headers_para):
        headers_data = pre_res["body"][headers_para[0]]
        #结果替换
        headers = Base.res_sub(headers,headers_data)
    if len(cookies_para):
        cookies_data = pre_res["body"][cookies_para[0]]
        # 结果替换
        cookies = Base.res_sub(headers, cookies_data)
    return headers,cookies


# 2. 参数化运行测试用例
class Test_Excel():
    # 初始化参数数据
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        except_result = case[data_key.except_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        status_code = case[data_key.status_code]
        db_verify = case[data_key.db_verify]

        # 1. 验证前置条件
        if pre_exec:
            pre_case = Data(case_file,sheet_name).get_case_pre(pre_exec)
            # 2. 执行前置测试用例，获取返回值
            pre_res = run_pre(pre_case)
            # 获取前置条件中返回的数据
            headers, cookies = get_correlation(headers, cookies, pre_res)

        # 判断headers和cookies是否存在
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        # # 请求接口
        r = run_api(url, method, params_type, header, cookie, params)
        print(r)
        # AssertUtil().assert_code(r["code"], expected_code=status_code)
        # AssertUtil().assert_in_body(r["body"], expected_body=except_result)


if __name__ == '__main__':
    pytest.main(["-s", "test_excel_case.py"])
