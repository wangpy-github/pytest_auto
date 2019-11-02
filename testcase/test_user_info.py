from config.Conf import get_data_path, ConfigYaml
import pytest
import os
from utils.YamlUtil import YamlReader
from utils.RequestsUtil import Request
"""
测试用例参数化
1. 获取测试用例内容list
2. 参数化执行测试用例
"""
test_file = os.path.join(get_data_path(), "test_userinfo.yml")
test_data_list = YamlReader(test_file).data_all()
@pytest.mark.parametrize("userinfo", test_data_list)
def test_userinfo(userinfo):
    url = ConfigYaml().get_conf_url() + userinfo["url"]
    data = userinfo["data"]
    print(data)
    print(type(data))
    r = Request().post(url, data=data)
    print(r)


if __name__ == '__main__':
    pytest.main(["-s", "test_user_info.py"])