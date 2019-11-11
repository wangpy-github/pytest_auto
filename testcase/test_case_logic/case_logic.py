#coding=utf-8
import json
from common.Base import Correlation


def logic(data_variable_list, pre_case_res, url, headers, cookies, params):
    """
    在有变量的情况下，此处填写组合数据的逻辑
    """
    if isinstance(data_variable_list, list) and len(data_variable_list) != 0:
        # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
        # 2. 提取到有用的数据之后，去替换excel的数据
        try:
            id = pre_case_res.get("get_brand")["body"]["data"][0]["id"]
            id = json.dumps(id)
            url = Correlation().res_sub(url, id)
            headers = Correlation().res_sub(headers, None)
            cookies = Correlation().res_sub(cookies, None)
            params = Correlation().res_sub(params, None)
            return url, headers, cookies, params
        except:
            pass
        try:
            id = pre_case_res.get("get_category")["body"]["data"][0]["id"]
            id = json.dumps(id)
            url = Correlation().res_sub(url, id)
            headers = Correlation().res_sub(headers, None)
            cookies = Correlation().res_sub(cookies, None)
            params = Correlation().res_sub(params, None)
            url = Correlation().res_sub(url, None)
            return url, headers, cookies, params
        except:
            pass
        try:
            id = pre_case_res.get("get_category")["body"]["data"][0]["id"]
            id = json.dumps(id)
            url = Correlation().res_sub(url, id)
            headers = Correlation().res_sub(headers, None)
            cookies = Correlation().res_sub(cookies, None)
            params = Correlation().res_sub(params, None)
            return url, headers, cookies, params
        except:
            pass
