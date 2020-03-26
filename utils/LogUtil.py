"""
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息
"""

import logging
from config import Conf
import datetime
from config.Conf import ConfigYaml
import os

# 定义日志等级的映射
log_l = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

"""
步骤：
日志输出到控制台或文件
1. 设置logger名称
2. 设置log级别
3. 创建handler，用于输出控制台或写入日志文件
4. 设置日志级别
5. 定义handler的输出格式
6. 添加handler
"""


class Logger():
    def __init__(self, log_name, log_file, log_level):
        self.log_name = log_name  # 之后作为参数
        self.log_file = log_file  # 写在配置文件
        self.log_level = log_level  # 写在配置文件
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_l[log_level])
        self.formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(lineno)d-%(message)s")
        # 判断handlers是否存在
        if not self.logger.handlers:
            # 创建输出控制台的handler
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[log_level])
            fh_stream.setFormatter(self.formatter)

            # 创建输出到文件的handler
            fh_file = logging.FileHandler(self.log_file)
            fh_file.setLevel(log_l[log_level])
            fh_file.setFormatter(self.formatter)

            # 添加handler
            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)


"""
定义对外的方法，参数只有log_name
"""
# 初始化参数数据
log_path = Conf.get_log_path()  # log目录路径
current_time = datetime.datetime.now().strftime("%Y-%m-%d")  # 当前年月日
log_extension = ConfigYaml().get_conf_log_extension()  # .log扩展名

logfile = os.path.join(log_path, current_time + log_extension)  # 拼接log文件的路径
loglevel = ConfigYaml().get_conf_log_level()  # log等级


# 对外方法
def my_log(log_name=__file__):
    return Logger(log_name=log_name, log_file=logfile, log_level=loglevel).logger


if __name__ == '__main__':
    my_log().info("hello word")
