# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  # 解决编码的问题
import json
from common.Base import Correlation


def logic(pre_res_more, case_id, url, headers, cookies, params):
    """
    在有变量的情况下，此处填写组合数据的逻辑，只填写有前置条件的测试用例
    其中， verif_data_pre 我将它称为期望结果，根据前置数据计算所得  Type：dict

    :param pre_res_more: 前置测试用例结果的字典
    :param case_id: excel读取的当前case_id
    :param url: excel读取的url
    :param headers: excel读取的headers
    :param cookies: excel读取的cookies
    :param params: excel读取的params
    :return: 
    """
    verif_data_pre = {}
    # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
    # 2. 提取到有用的数据之后，去替换excel的数据
    if case_id == "create_cart":
        # 1. 取数据。组合数据
        goods_id = pre_res_more["goods_detail"]["body"]["data"]["goods_id"]
        goods_id = json.dumps(goods_id)
        # 2. 替换数据
        params = Correlation().res_sub(params, goods_id)
    if case_id == "checkOrder":
        rec_id = pre_res_more["create_cart"]["body"]["data"]["cart_list"][0]["goods_list"][0]["rec_id"]
        rec_id = json.dumps(rec_id)
        params = Correlation().res_sub(params, rec_id)
    if case_id == "done":
        rec_id = pre_res_more["checkOrder"]["body"]["data"]["goods_list"][0]["rec_id"]
        pay_id = pre_res_more["checkOrder"]["body"]["data"]["payment_list"][2]["pay_id"]
        shipping_id = pre_res_more["checkOrder"]["body"]["data"]["shipping_list"][0]["shipping_id"]
        rec_id = json.dumps(rec_id)
        pay_id = json.dumps(pay_id)
        shipping_id = json.dumps(shipping_id)
        params = Correlation().res_sub(params, rec_id, pay_id, shipping_id)
    if case_id == "confirm" or case_id == "ship" or case_id == "goods_service_to_user":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookie = json.dumps(cookie)  # str
        order_id = str(order_id)  # str
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    return url, headers, cookies, params, verif_data_pre