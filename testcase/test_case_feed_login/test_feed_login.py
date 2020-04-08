# coding=utf-8
import pytest
from common import Base
from common.Base import run_api
from common.ExcelConfig import DataConfig
from testcase.common.excel_case_common import Base_Excel_Test
from testcase.common.init_env_msg import InitConfMsg
from testcase.test_case_feed_login.feed_login import logic
from utils.LogUtil import my_log

log = my_log()
data_key = DataConfig
request_params = dict()

# 初始化环境信息
env_msg = InitConfMsg(env="feed_dev", excel_filename="test_data.xlsx", sheet_name="用户信息")
env_url = env_msg.env_url
case_file = env_msg.case_file
data_list = env_msg.data_list
env_excel_sheet = env_msg.env_excel_sheet


class Test_Feed_login(Base_Excel_Test):
    env_url = env_url
    env_excel_sheet = env_excel_sheet
    case_file = case_file

    # @pytest.mark.timeout(0.03)  # 当前用例限定0.03s超时
    # @pytest.mark.flaky(reruns=3, reruns_delay=1)  # 如果失败则延迟1s后重跑
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        super().test_run(case)

    def run(self, case, res_more=None):
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
        url, headers, cookies, params, verif_data_pre = logic(res_more, case_id=case_id, url=url, headers=headers,
                                                              cookies=cookies, params=params)

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
