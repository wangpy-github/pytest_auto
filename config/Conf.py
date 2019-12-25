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
# 定义conf.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_conf.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义logs目录路径
_log_path = BASE_DIR + os.sep + "logs"
# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"
# 定义env_conf文件路径
_env_conf_path = _config_path + os.sep + "env_conf.yml"


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


############获取环境信息############
class Env_conf():
    def __init__(self, env_alise):
        """
        :param env_alise: 环境别名
        """
        self.env_config = YamlReader(get_env_conf_path()).data()
        self.env_alise = env_alise

    # 获取环境配置信息
    def get_conf_url(self):
        return self.env_config[self.env_alise]["url"]

    # 获取测试用例文件的名称
    def get_excel_file(self):
        return self.env_config[self.env_alise]["test_case_file"]

    # 定义获取excel_sheet名称
    def get_excel_sheet(self):
        return self.env_config[self.env_alise]["case_sheet"]

    # 定义获取公共变量token的方法
    def get_common_variable(self):
        return self.env_config[self.env_alise]["common_variable"]


if __name__ == '__main__':
    # print(get_config_file())
    env = Env_conf("test")
    print(env.get_conf_url())
    print(env.get_excel_file())
    print(env.get_excel_sheet())
    print(env.get_common_variable())

    # print(ConfigYaml().get_conf_log_level())
    # print(ConfigYaml().get_conf_log_extension())
    # print(ConfigYaml().get_db_config_info("db_01"))