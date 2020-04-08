#coding=utf-8
import os
from utils.YamlUtil import YamlReader

"""
获取项目目录
"""
# 获取项目路径
current_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current_path))
# 定义config目录路径 以及 data目录路径
_config_path = BASE_DIR + os.sep + "config"
_data_path = BASE_DIR + os.sep + "data"
# 定义 conf.yml db_conf.yml env_config.yml logs目录 report目录 路径
_config_file = _config_path + os.sep + "conf.yml"
_db_config_file = _config_path + os.sep + "db_conf.yml"
_env_conf_path = _config_path + os.sep + "env_config.yml"
_log_path = BASE_DIR + os.sep + "logs"
_report_path = BASE_DIR + os.sep + "report"


def get_env_conf_path():
    return _env_conf_path


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


class ConfigYaml():
    """
    读取文件信息
    """

    # 初始读取yaml配置文件内容
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()
        self.env_config = YamlReader(get_env_conf_path()).data()

    """
    定义一些获取配置文件指定信息的方法
    """

    # 获取日志等级
    def get_conf_log_level(self):
        return self.config["log_level"]

    # 获取log文件的扩展名
    def get_conf_log_extension(self):
        return self.config["log_extension"]

    # 获取db_config相关信息
    def get_db_config_info(self, db_alise):
        return self.db_config[db_alise]

    # 获取环境url
    def get_conf_url(self, env_alise):
        return self.env_config[env_alise]["url"]

    # 获取测试用例文件的名称
    def get_excel_file(self, env_alise):
        return self.env_config[env_alise]["test_case_file"]

    # 获取excel_sheet名称
    def get_excel_sheet(self, env_alise):
        return self.env_config[env_alise]["case_sheet"]

    # 定义获取环境公共变量的方法
    def get_common_variable(self, env_alise):
        return self.env_config[env_alise]["common_variable"]


if __name__ == '__main__':
    a = ConfigYaml().get_excel_file("dev")
    print(a)
