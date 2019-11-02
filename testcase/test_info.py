import pytest
from utils.RequestsUtil import Request
from utils.AssertUtil import AssertUtil

class Test_Info():

    def test_info(self):
        data = {
            "json": '{"token": "3933241097da4ef47c9f8e7458dfd5624d116237"}'
        }
        res = Request().post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
        code = res["code"]
        AssertUtil().assert_code(code, 201)
        print(res)


if __name__ == '__main__':
    pytest.main(["-s", "test_info.py"])
