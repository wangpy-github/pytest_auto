from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql
import json
import re
from common.ExcelConfig import DataConfig
from utils.RequestsUtil import Request
from distutils.log import Log
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


def run_pre(pre_case):
    """
    执行前置测试用例
    """
    # 初始化前置条件测试用例的参数
    url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
    method = pre_case[data_key.method]
    params = pre_case[data_key.params]
    params_type = pre_case[data_key.params_type]
    headers = pre_case[data_key.headers]
    cookies = pre_case[data_key.cookies]
    # 判断headers和cookies是否存在
    header = json_parse(headers)
    cookie = json_parse(cookies)
    params = json_parse(params)
    r = run_api(url, method=method, params_type=params_type, header=header, cookie=cookie, params=params)
    return r


def get_correlation(headers, cookies, params, pre_res):
    # 验证是否有关联
    headers_para, cookies_para, params_para = params_find(headers, cookies, params)
    # TODO 可能还会用到body里边的数据，到时候再定义
    # 有关联，获取上个接口返回的关联数据
    if isinstance(cookies_para, list):  # TODO 如果参数本身就是一个列表，会出问题
        cookie = pre_res["cookies"]
        cookie = json.dumps(cookie)
        # 结果替换
        cookies = res_sub(cookies, cookie)
    return headers, cookies, params


if __name__ == '__main__':
    print(init_db("db_01"))
