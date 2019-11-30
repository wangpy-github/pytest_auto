from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql
import json
import re
from common.ExcelConfig import DataConfig
from utils.RequestsUtil import Request
from distutils.log import Log
import subprocess
"""
定义公共方法，用来返回mysql连接对象

1. 通过配置初始化数据库信息
2. 初始化mysql对象
"""
def init_db(db_alise):
    # 初始化数据库配置信息
    db_info = ConfigYaml().get_db_config_info(db_alise)
    host = db_info["db_host"]
    user = db_info["db_user"]
    port = int(db_info["db_port"])
    password = db_info["db_password"]
    database = db_info["db_database"]
    charset = db_info["db_charset"]
    # 初始化数据库游标对象
    conn = Mysql(host=host,user=user,password=password,database=database,charset=charset,port=port)
    return conn

# 格式化字符串,转换为dict
def json_parse(data):
    # if headers:
    #     header = json.loads(headers)
    # else:
    #     header = headers
    return json.loads(data) if data else data

data_key = DataConfig
log = Log()
def run_api(url, method, params_type, header=None, cookie=None, params=None):
    """
    发送api请求
    """
    request = Request()
    if str(method).lower() == "get":
        r = request.get(url, headers=header, cookies=cookie)
    elif str(method).lower() == "post":
        if str(params_type).lower() == "form_data":
            r = request.post(url, data=params, headers=header, cookies=cookie)
        elif str(params_type).lower() == "json":
            r = request.post(url, json=params, headers=header, cookies=cookie)
    else:
        log.error("错误请求methods：", method)
    return r



class Correlation():
    def res_find(self, data, pattern_data=r'\${(.*?)}\$'):
        """
        查询
        :param data: 将被正则匹配的字符串
        :param pattern_data: 正则表达式
        """
        pattern = re.compile(pattern_data)
        re_res = pattern.findall(data)
        return re_res

    def params_find(self, data):
        if "${" in data:
            data = self.res_find(data)
        return data

    def res_sub(self, data, *args, pattern_data=r'\${(.*?)}\$'):
        """
        注意：数据的顺序不能错
        作用：有变量就替换，没有则返回原数据
        :param data: 将被替换的字符串
        :param args: 去替换的目标值元组
        """
        pattern = re.compile(pattern_data)
        re_res_list = pattern.findall(data)
        if re_res_list and len(re_res_list)!=0:
            for val in args:
                data = re.sub(pattern_data, val, data, count=1)
        return data

if __name__ == '__main__':
    print(init_db("db_01"))
