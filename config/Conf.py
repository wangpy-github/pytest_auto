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
# 定义config.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"


def get_config_path():
    return _config_path


def get_config_file():
    return _config_file


"""
读取文件信息
"""
class ConfigYaml():
    # 初始读取yaml配置文件内容
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()

    """
    定义一些获取配置文件指定信息的方法
    """
    def get_conf_url(self):
        return self.config["BASE"]["test"]["url"]


if __name__ == '__main__':
    print(get_config_file())
    print(ConfigYaml().get_conf_url())
