#coding=utf-8
import json
from common.Base import Correlation


def logic(pre_case_res, case_id, url, headers, cookies, params):
    """
    在有变量的情况下，此处填写组合数据的逻辑
    """
    # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
    # 2. 提取到有用的数据之后，去替换excel的数据
    if case_id == "get_brand_detail_1":
        # 1. 取数据，组合数据
        id = pre_case_res.get("get_brand")["body"]["data"][0]["id"]
        id = json.dumps(id)
        # 2. 替换数据
        url = Correlation().res_sub(url, id)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, None)
        return url, headers, cookies, params

    if case_id == "get_category_detail_1":
        id = pre_case_res.get("get_category")["body"]["data"][0]["id"]
        id = json.dumps(id)
        url = Correlation().res_sub(url, id)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, None)
        url = Correlation().res_sub(url, None)
        return url, headers, cookies, params
