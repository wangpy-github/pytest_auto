import os
from utils.YamlUtil import YamlReader

"""
获取项目目录
"""
# 获取项目路径
current_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current_path))
# 定义config目录路径
_config_path = BASE_DIR + os.sep + "config"
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# 定义config.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_config.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义logs目录路径
_log_path = BASE_DIR + os.sep + "logs"
# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"
# 定义testcase目录路径
_testcase_path = BASE_DIR + os.sep + "testcase"

def get_testcase_path():
    return _testcase_path

def get_data_path():
    return _data_path


def get_config_path():
    return _config_path


def get_config_file():
    return _config_file


def get_log_path():
    return _log_path


def get_db_config_file():
    return _db_config_file

def get_report_path():
    return _report_path

"""
读取文件信息
"""


class ConfigYaml():
    # 初始读取yaml配置文件内容
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    """
    定义一些获取配置文件指定信息的方法
    """

    # 获取url
    def get_conf_url(self):
        return self.config["BASE"]["test"]["url"]

    # 获取日志等级
    def get_conf_log_level(self):
        return self.config["BASE"]["log_level"]

    # 获取log文件的扩展名
    def get_conf_log_extension(self):
        return self.config["BASE"]["log_extension"]

    # 获取db_config相关信息
    def get_db_config_info(self, db_alise):
        return self.db_config[db_alise]

    # 获取测试用例文件的名称
    def get_excel_file(self):
        return self.config["BASE"]["test"]["test_case_file"]

    # 定义获取excel_sheet名称
    def get_excel_sheet(self):
        return self.config["BASE"]["test"]["case_sheet"]


if __name__ == '__main__':
    # print(get_config_file())
    # print(ConfigYaml().get_conf_url())
    # print(ConfigYaml().get_conf_log_level())
    # print(ConfigYaml().get_conf_log_extension())
    # print(ConfigYaml().get_db_config_info("db_01"))
    print(ConfigYaml().get_excel_file())
    print(ConfigYaml().get_excel_sheet())