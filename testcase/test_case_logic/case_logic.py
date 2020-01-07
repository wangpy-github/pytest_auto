# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  # 解决编码的问题
import json
import time
from common.Base import Correlation, init_db
from config.Conf import Env_conf

# 获取公共变量
token = Env_conf("test").get_common_variable()["token"]

def logic(pre_res_more, case_id, url, headers, cookies, params):
    """
    在有变量的情况下，此处填写组合数据的逻辑，只填写有前置条件的测试用例，数据格式不用管，已经自动转换
    其中， verif_data_pre 我将它称为期望结果，根据前置数据计算所得  Type：list
    注意：一条case_id， 一条if语句，以免验证verif_data_pre时出错！
    :param pre_res_more: 前置测试用例结果的字典
    :param case_id: excel读取的当前case_id
    :param url: excel读取的url
    :param headers: excel读取的headers
    :param cookies: excel读取的cookies
    :param params: excel读取的params
    :return: 
    """
    # 期望结果列表
    verif_data_pre = []
    # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
    # 2. 提取到有用的数据之后，去替换excel的数据
    if case_id == "goods_detail":
        params = Correlation().res_sub(params, token)
    if case_id == "create_cart":
        # 1. 取数据，组合数据
        goods_id = pre_res_more["goods_detail"]["body"]["data"]["goods_id"]
        # 2. 替换数据
        params = Correlation().res_sub(params, token, goods_id)
    if case_id == "checkOrder":
        rec_id = pre_res_more["create_cart"]["body"]["data"]["cart_list"][0]["goods_list"][0]["rec_id"]
        params = Correlation().res_sub(params, token, rec_id)
    if case_id == "done":
        rec_id = pre_res_more["checkOrder"]["body"]["data"]["goods_list"][0]["rec_id"]
        pay_id = pre_res_more["checkOrder"]["body"]["data"]["payment_list"][2]["pay_id"]
        shipping_id = pre_res_more["checkOrder"]["body"]["data"]["shipping_list"][0]["shipping_id"]
        params = Correlation().res_sub(params, token, rec_id, pay_id, shipping_id)
    if case_id == "wxpay":
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]
        params = Correlation().res_sub(params, token, order_id)
        # 更改数据库数据
        conn = init_db("db_01")
        conn.exec("UPDATE hs_order_info SET pay_status=2 WHERE order_id={}".format(order_id))
    if case_id == "confirm":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "ship":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "goods_service_to_user":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "affirmReceived":
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]
        order_id = str(order_id)
        params = Correlation().res_sub(params, token, order_id)
    if case_id == "cancel":
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]
        params = Correlation().res_sub(params, token, order_id)
    if case_id == "wxpay_1":
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]
        params = Correlation().res_sub(params, token, order_id)
    if case_id == "confirm_1":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "ship_1":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "goods_service_to_user_1":
        cookie = pre_res_more["login"]["cookies"]    # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    if case_id == "integral":
        params = Correlation().res_sub(params, token)
    if case_id == "integral_pay":
        time.sleep(2)   # 支付过快：提示处理中，导致验证积分时断言错误
        params = Correlation().res_sub(params, token)
    if case_id == "integral_1":
        # 处理后续断言的数据
        integral = pre_res_more["integral"]["body"]["data"]["integral"]
        integral = int(integral) - 10
        integral = str(integral)
        data_pre = "'integral': {}".format(integral)
        verif_data_pre.append(data_pre)
        params = Correlation().res_sub(params, token)
    if case_id == "serve":
        params = Correlation().res_sub(params, token)
    if case_id == "address_list":
        params = Correlation().res_sub(params, token)
    if case_id == "change_price":
        params = Correlation().res_sub(params, token)
    if case_id =="serve_confirm":
        pet_id = str(pre_res_more["serve"]["body"]["data"]["pet_list"][0]["id"])
        address_id = str(pre_res_more["address_list"]["body"]["data"][0]["id"])
        time_1 = pre_res_more["serve"]["body"]["data"]["time_list"][0]["date"]
        params = Correlation().res_sub(params, token, pet_id, address_id, time_1)
    if case_id == "serve_done":
        pet_id = str(pre_res_more["serve"]["body"]["data"]["pet_list"][0]["id"])
        address_id = str(pre_res_more["address_list"]["body"]["data"][0]["id"])
        time_1 = pre_res_more["serve"]["body"]["data"]["time_list"][0]["date"]
        params = Correlation().res_sub(params, token, pet_id, address_id, time_1)
    if case_id == "serve_order_cancel":
        order_sn = pre_res_more["serve_done"]["body"]["data"]["order_sn"]
        params = Correlation().res_sub(params, token, order_sn)
    if case_id == "serve_confirm_1":
        pet_id = str(pre_res_more["serve"]["body"]["data"]["pet_list"][0]["id"])
        address_id = str(pre_res_more["address_list"]["body"]["data"][1]["id"])
        time_1 = pre_res_more["serve"]["body"]["data"]["time_list"][0]["date"]
        params = Correlation().res_sub(params, token, pet_id, address_id, time_1)
    if case_id == "serve_confirm_2":
        pet_id = str(pre_res_more["serve"]["body"]["data"]["pet_list"][0]["id"])
        time_1 = str(pre_res_more["serve"]["body"]["data"]["time_list"][0]["date"])
        params = Correlation().res_sub(params, token, pet_id, time_1)
    if case_id == "serve_confirm_3":
        addres_id = str(pre_res_more["address_list"]["body"]["data"][1]["id"])
        time_1 = str(pre_res_more["serve"]["body"]["data"]["time_list"][0]["date"])
        params = Correlation().res_sub(params, token, addres_id, time_1)
    if case_id == "serve_confirm_4":
        pet_id = str(pre_res_more["serve"]["body"]["data"]["pet_list"][0]["id"])
        addres_id = str(pre_res_more["address_list"]["body"]["data"][1]["id"])
        params = Correlation().res_sub(params, token, pet_id, addres_id)
    if case_id == "serve_order_pay":
        order_sn = pre_res_more["serve_done"]["body"]["data"]["order_sn"]
        params = Correlation().res_sub(params, token, order_sn)
        # 更改数据库数据
        conn = init_db("db_01")
        conn.exec("UPDATE hs_serve_order_info SET order_status=3, pay_status=1, store_id=30 WHERE order_sn={}".format(order_sn))
    return url, headers, cookies, params, verif_data_pre