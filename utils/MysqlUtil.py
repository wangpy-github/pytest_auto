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
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

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
