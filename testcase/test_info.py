import pytest
from utils.RequestsUtil import Request
from utils.AssertUtil import AssertUtil
from common.Base import init_db

class Test_Info():

    def test_info(self):
        data = {
            "json": '{"token": "3933241097da4ef47c9f8e7458dfd5624d116237"}'
        }
        # Resquest()工具类使用
        res = Request().post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
        code = res["code"]
        # 断言工具类使用
        AssertUtil().assert_code(code, 200)
        # 数据库工具类使用
        conn = init_db("db_01")
        r = conn.fetchone("select * from hs_order_info WHERE user_id=8;")
        assert r["user_id"] == res["body"]["data"]["id"]


if __name__ == '__main__':
    pytest.main(["-s", "test_info.py"])
