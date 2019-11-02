import logging

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
        self.log_name = log_name    # 之后作为参数
        self.log_file = log_file    # 写在配置文件
        self.log_level = log_level  # 写在配置文件
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_l[log_level])
        self.formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
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


if __name__ == '__main__':
    log = Logger("demo", "./a.log", "debug")
    log.logger.info("nihao")