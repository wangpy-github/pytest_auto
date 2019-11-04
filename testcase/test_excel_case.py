import os
from config.Conf import ConfigYaml
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
from utils.RequestsUtil import Request

"""
测试用例excel参数化
步骤：
1. 初始化信息
    1. 初始化测试用例文件
    2. 测试用例sheet名称
    3. 获取需要运行的测试用例数据
    4. log日志
2. 测试用例方法，参数化运行
"""

# 1. 初始化信息
case_file = os.path.join("../data",ConfigYaml().get_excel_file())
sheet_name = ConfigYaml().get_excel_sheet()
data_list = Data(case_file, sheet_name).get_run_data()
# print(data_list)
log = my_log()
# 2. 参数化运行测试用例
class TestExcel():
    def test_user_info(self):
        data_key = DataConfig
        url = ConfigYaml().get_conf_url() + data_list[0][data_key.url]
        print(url)
        params = data_list[0][data_key.params]
        print(params)
        r = Request().post(url, data=params)
        print(r)

if __name__ == '__main__':
    TestExcel().test_user_info()


