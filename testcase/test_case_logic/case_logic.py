# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  # 解决编码的问题
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
        id = pre_case_res["body"]["data"][0]["id"]
        id = json.dumps(id)
        # 2. 替换数据
        url = Correlation().res_sub(url, id)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, None)
        return url, headers, cookies, params

    if case_id == "get_category_detail_1":
        id = pre_case_res.get["body"]["data"][0]["id"]
        id = json.dumps(id)
        url = Correlation().res_sub(url, id)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, None)
        url = Correlation().res_sub(url, None)
        return url, headers, cookies, params
    if case_id == "create_cart":
        goods_id = pre_case_res["body"]["data"]["goods_id"]
        goods_id = json.dumps(goods_id)
        url = Correlation().res_sub(url,None)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, goods_id)
        url = Correlation().res_sub(url, None)
        return url, headers, cookies, params

    if case_id == "checkOrder":
        rec_id = pre_case_res["body"]["data"]["cart_list"][0]["goods_list"][0]["rec_id"]
        rec_id = json.dumps(rec_id)
        url = Correlation().res_sub(url,None)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, rec_id)
        url = Correlation().res_sub(url, None)
        return url, headers, cookies, params
    if case_id == "done":
        rec_id = pre_case_res["body"]["data"]["goods_list"][0]["rec_id"]
        pay_id = pre_case_res["body"]["data"]["payment_list"][0]["pay_id"]
        shipping_id = pre_case_res["body"]["data"]["shipping_list"][0]["shipping_id"]
        rec_id = json.dumps(rec_id)
        pay_id = json.dumps(pay_id)
        shipping_id = json.dumps(shipping_id)
        url = Correlation().res_sub(url,None)
        headers = Correlation().res_sub(headers, None)
        cookies = Correlation().res_sub(cookies, None)
        params = Correlation().res_sub(params, rec_id, pay_id, shipping_id)
        url = Correlation().res_sub(url, None)
        return url, headers, cookies, params