from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql
import json
import re

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

def res_find(data,pattern_data= r'\${(.*)}\$'):
    """
    查询
    :param data: 将被正则匹配的字符串
    :param pattern_data: 正则表达式
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res

def res_sub(data,replace,pattern_data= r'\${(.*)}\$'):
    """
    替换
    :param data: 要被替换的字符串
    :param replace: 被替换的字符串
    :param pattern_data: 正则表达式
    :return: 
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data, replace, data)
    return re_res

def params_find(headers, cookies, params):
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    if "${" in params:
        params = res_find(params)
    # 返回${}$中的自定义[变量名]，没有${}$则返回excel中原数据
    return headers, cookies, params




if __name__ == '__main__':
    print(init_db("db_01"))
