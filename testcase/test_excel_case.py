import os
from config.Conf import ConfigYaml, get_data_path
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
import pytest
from utils.AssertUtil import AssertUtil
from common import Base
from common.Base import run_pre, get_correlation, run_api
import allure
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
case_file = get_data_path() + os.sep + ConfigYaml().get_excel_file()  # 使用绝对路径
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file, sheet_name).get_run_data()  # 获取需要运行的测试用例
log = my_log()
data_key = DataConfig

# 2. 参数化运行测试用例
class Test_Excel():
    # 初始化参数数据
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        except_result = case[data_key.except_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        status_code = case[data_key.status_code]
        db_verify = case[data_key.db_verify]

        # 验证前置条件
        if pre_exec:
            pre_case = Data(case_file, sheet_name).get_case_pre(pre_exec)
            # 2. 执行前置测试用例，获取返回值
            pre_res = run_pre(pre_case)
            # 获取前置条件中返回的关联数据
            # 查看哪些数据有关联，取到关联的数据并与当前数据组合
            cookies = get_correlation(cookies, pre_res)

        # 判断headers, cookies, params是否存在,存在则转为dict
        try:
            header = Base.json_parse(headers)
            cookie = Base.json_parse(cookies)
            params = Base.json_parse(params)
        except Exception as e:
            log.error("参数格式不对", e)
            raise
        # 请求接口
        r = run_api(url, method, params_type, header, cookie, params)
        """
        allure:
        1. 一级标签（feature）：sheet名称
        2. 二级标签（story）：模块
        3. 用例标题（title）：用例id + 接口名称
        4. 用例描述（description）：请求url + 请求类型 + 期望结果 + 实际结果
        """
        allure.dynamic.feature(sheet_name)
        allure.dynamic.story(case_model)
        title = "{} {}".format(case_id, case_name)
        allure.dynamic.title(title)
        desc = "<font color='red'>请求URL:</font> {}<Br/>" \
               "<font color='red'>请求类型:</font>{}<Br/>" \
               "<font color='red'>期望结果:</font>{}<Br/>" \
               "<font color='red'>实际结果:</font>{}".format(url, method, except_result, r)
        allure.dynamic.description(desc)
        # AssertUtil().assert_code(r["code"], expected_code=status_code)
        # AssertUtil().assert_in_body(r["body"], expected_body=except_result)


if __name__ == '__main__':
    pytest.main(["-s", "test_excel_case.py"])
