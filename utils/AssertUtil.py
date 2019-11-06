#coding=utf-8
from utils.LogUtil import my_log
import json

"""
定义封装断言类，用来断言 code 和 body
步骤：
1. 初始化数据，用来打印日志
2. 断言code相等
3. 断言body相等
4. 断言body包含
"""


class AssertUtil():
    def __init__(self):
        self.log = my_log("AssertUtil")

    # 断言code相等
    def assert_code(self, code, expected_code):
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error, code is %s, expected_code is %s" % (code, expected_code))
            raise

    # 断言body相等
    def assert_body(self, body, expected_body):
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("body error, body is %s, expected_body is %s" % (body, expected_body))
            raise

    # 断言body是否包含期待的expected_body
    def assert_in_body(self, body, expected_body):
        try:
            body = json.dumps(body, ensure_ascii=False)
            assert expected_body in body
            return True
        except:
            self.log.error("不包含或者body是错误的, body is %s, expected_body is %s" % (body, expected_body))
            raise
