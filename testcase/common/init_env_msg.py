# coding=utf-8
import os
from common.ExcelData import Data
from config.Conf import ConfigYaml, get_data_path


class InitConfMsg():
    """
    初始化配置信息，并获取要运行的case数据
    """

    def __init__(self, env=None, excel_filename=None, sheet_name=None):
        # 1. 初始化信息，可单独定义或者写成配置文件
        conf = ConfigYaml()
        self.env_url = conf.get_conf_url(env)
        self.env_excel_file = conf.get_excel_file(env).get(excel_filename)
        self.env_excel_sheet = conf.get_excel_sheet(env).get(sheet_name)
        self.case_file = get_data_path() + os.sep + self.env_excel_file
        # 2. 获取需要运行的测试用例数据
        self.data_list = Data(self.case_file, self.env_excel_sheet).get_run_data()


if __name__ == '__main__':
    env = InitConfMsg(env="feed_dev", excel_filename="test_data.xlsx", sheet_name="用户信息")
    print(env.env_url)
