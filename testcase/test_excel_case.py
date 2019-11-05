import os
from config.Conf import ConfigYaml, get_data_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
from utils.RequestsUtil import Request
import json
import pytest

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
"""
# 1. 初始化信息，可单独定义或者写成配置文件
# case_file = os.path.join("/data", ConfigYaml().get_excel_file())    # 相对路径，使用pytest会出错
case_file = get_data_path() + os.sep + ConfigYaml().get_excel_file()  # 使用绝对路径
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file, sheet_name).get_run_data()
log = my_log()
# 2. 参数化运行测试用例
class Test_Excel():
    # 初始化参数数据
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        data_key = DataConfig
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
        # 接口请求
        if headers:
            header = json.loads(headers)
        else:
            header = headers
        if cookies:
            cookie = json.loads(cookies)
        else:
            cookie = cookies
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        if str(method).lower() == "get":
            r = Request().get(url, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            if str(params_type).lower() == "form_data":
                r = Request().post(url, data=params, headers=header, cookies=cookie)
            elif str(params_type).lower() == "json":
                r = Request().post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求methods：", method)
        print(r)

if __name__ == '__main__':
    pytest.main(["-s", "test_excel_case.py"])
