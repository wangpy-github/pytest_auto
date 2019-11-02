from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql

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
    # 初始化数据库连接对象
    conn = Mysql(host=host,user=user,password=password,database=database,charset=charset,port=port)
    return conn


if __name__ == '__main__':
    print(init_db("db_01"))
