import os
import zipfile
from config.Conf import ConfigYaml, get_report_path
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
        if str(params_type).lower() == "query_string":
            r = request.get(url, headers=header, data=params, cookies=cookie)
        else:
            r = request.get(url, headers=header, cookies=cookie)
    elif str(method).lower() == "post":
        if str(params_type).lower() == "form_data":
            r = request.post(url, data=params, headers=header, cookies=cookie)
        elif str(params_type).lower() == "json":
            r = request.post(url, json=params, headers=header, cookies=cookie)
    elif str(method).lower() == "put":
        if str(params_type).lower() == "form_data":
            r = request.put(url, data=params, headers=header, cookies=cookie)
        elif str(params_type).lower() == "json":
            r = request.post(url, json=params, headers=header, cookies=cookie)
    elif str(method).lower() == "delete":
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
        作用：1. 有变量就替换，没有则返回原数据
              2. 数据格式转换：dict转为josn_str，其他则转换为str
        :param data: 将被替换的字符串
        :param args: 去替换的目标值元组
        """
        pattern = re.compile(pattern_data)
        re_res_list = pattern.findall(data)
        if re_res_list and len(re_res_list)!=0:
            for val in args:
                if isinstance(val, dict):
                    data = re.sub(pattern_data, json.dumps(val), data, count=1)
                data = re.sub(pattern_data, str(val), data, count=1)
        return data


def allure_report(report_path, report_html):
    """
    生成allure 报告
    """
    # 执行命令 allure generate <allure测试结果目录> -o <存放报告的目录> --clean
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    log.info("报告地址")
    try:
        subprocess.call(allure_cmd, shell=True)
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise

def zip_new_report():
    """
    获取最新生成的测试报告路径，并把整个文件夹内的文件打包，并将zip的路径返回
    """
    # 1. 获取最新的测试报告路径
    report_path = get_report_path()
    html_path = os.path.join(report_path, "html")
    list_report_htmls = os.listdir(html_path)
    # 按照目录的创建时间升序排列
    list_report_htmls.sort(key=lambda file: os.path.getmtime(os.path.join(html_path, file)))
    new_report_path = os.path.join(html_path, list_report_htmls[-1])
    # 2. 把整个文件夹内的文件打包
    # target_zip_path：存放zip的目录
    target_zip_path = os.path.join(report_path, list_report_htmls[-1]+".zip")
    f = zipfile.ZipFile(target_zip_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(new_report_path):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()
    return target_zip_path


if __name__ == '__main__':
    print(init_db("db_01"))
    new_zip_report_path = zip_new_report()
