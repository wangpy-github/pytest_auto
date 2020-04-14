# coding=utf-8
import pytest
from common import Base
from common.Base import run_api
from common.ExcelConfig import DataConfig
from testcase.common.excel_case_common import Base_Excel_Test
from testcase.common.init_env_msg import InitConfMsg
from testcase.test_case_module_login.login_logic import logic
from utils.LogUtil import my_log

log = my_log()
data_key = DataConfig

# 初始化环境信息
env_msg = InitConfMsg(env="dev", excel_filename="test_data.xlsx", sheet_name="帖子")

# 测试类
class Test_login(Base_Excel_Test):
    env_url = env_msg.env_url
    env_excel_sheet = env_msg.env_excel_sheet
    case_file = env_msg.case_file
    data_list = env_msg.data_list

    # @pytest.mark.timeout(0.03)  # 当前用例限定0.03s超时
    # @pytest.mark.flaky(reruns=3, reruns_delay=1)  # 如果失败则延迟1s后重跑
    @pytest.mark.parametrize("case", data_list)
    def test_run(self, case):
        super().test_run(case)

    def run(self, case, res_more=None):
        url = self.env_url + case[data_key.url]
        case_id = case[data_key.case_id]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]

        """
        根据前置接口的返回数据，去获取当前接口的请求参数
        有${}$则处理，无则原数据返回
        """
        url, headers, cookies, params, verif_data_pre, verif_db = logic(res_more, case_id=case_id, url=url,
                                                                        headers=headers,
                                                                        cookies=cookies, params=params)

        """
        对接口返回正确的数据做处理，组织当前接口的数据
        1. str格式转换为dict，接口执行，并获取该接口返回数据
        2. 对当前接口返回的部分数据做allure展示使用
        3. 对期望的结果，包含返回数据及数据库期望数据放在r中一并返回，做断言准备
        """
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        param = Base.json_parse(params)

        # 执行当前用例
        r = run_api(url, method, params_type, header, cookie, param)
        # 组织请求参数，用于之后的allure描述展示
        r["requests_url"] = url
        r["requests_headers"] = header
        r["requests_cookies"] = cookie
        r["requests_params"] = param
        # 将需要验证的数据放在响应结果里边，用于之后的断言
        r["verif_data_pre"] = verif_data_pre if verif_data_pre else None
        r["verif_db"] = verif_db if verif_db else None
        return r  # 返回最终preA的结果
