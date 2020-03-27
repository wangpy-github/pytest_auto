"""
PyMySQL安装:pip3 install pymysql
使用：
    # 导入pymysql模块
    import pymysql
    # 连接database
    conn = pymysql.connect(
    host=“数据库地址”,
    user=“用户名”,
    password=“密码”,
    database=“数据库名”,
    charset=“utf8”)
    # 获取执行SQL语句的光标对象
    cursor = conn.cursor() # 结果集默认以元组显示
    # 获取执行SQL语句，结果作为字典返回
    #cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 定义要执行的SQL语句
    sql = "select username,password from tb_users"
    # 执行SQL语句
    cursor.execute(sql)
    # 执行
    cursor.fetchone()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
"""
import pymysql
from utils.LogUtil import my_log

"""
步骤：
1. 初始化数据
2. 创建查询、执行方法
3. 关闭对象
"""


class Mysql():
    # 初始化数据库连接，及日志
    def __init__(self, host, user, password, database, charset, port=3306):
        self.log = my_log("Mysql")
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset=charset
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)   # 此处设置默认返回元组改为字典

    # 关闭对象
    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    # 查询一条
    def fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 查询全部
    def fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 执行数据库
    def exec(self, sql):
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.log.error("Mysql 执行失败")
            self.log.error("Mysql执行错误信息：%s" % (e))
            return False
        return True


if __name__ == '__main__':
    sql = "select * from hs_order_info WHERE user_id=8;"
    mysql = Mysql(
        host="212.64.57.50",
        user="dev",
        password="Scp3908!op",
        database="house_dev",
        charset="utf8"
    )
    r = mysql.fetchone(sql)
    print(r)
