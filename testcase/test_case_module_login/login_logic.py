# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  # 解决编码的问题
import time
from common.Base import Correlation, init_db

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

    verif_data_pre = []   # 期望接口返回结果列表
    verif_db = []         # 期望数据库查询到的结果列表

    # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
    # 2. 提取到有用的数据之后，去替换excel的数据
    if case_id == "login":
        pass
    elif case_id == "post":
        # 1. 重前置条件的结果中取数据，并组合当前接口数据
        token = pre_res_more["login"]["body"]["data"]["token"]
        # 2. 替换数据
        headers = Correlation().res_sub(headers, token)
    elif case_id == "confirm_1":
        cookie = pre_res_more["login"]["cookies"]  # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    elif case_id == "ship_1":
        cookie = pre_res_more["login"]["cookies"]  # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    elif case_id == "goods_service_to_user_1":
        cookie = pre_res_more["login"]["cookies"]  # dict
        order_id = pre_res_more["done"]["body"]["data"]["order_id"]  # int
        cookies = Correlation().res_sub(cookies, cookie)
        params = Correlation().res_sub(params, order_id)
    elif case_id == "integral":
        params = Correlation().res_sub(params)
    elif case_id == "integral_pay":
        time.sleep(2)  # 支付过快：提示处理中，导致验证积分时断言错误
        params = Correlation().res_sub(params)
    elif case_id == "integral_1":
        # 处理后续断言的数据
        integral = pre_res_more["integral"]["body"]["data"]["integral"]
        integral = int(integral) - 10
        integral = str(integral)
        data_pre = "'integral': {}".format(integral)
        verif_data_pre.append(data_pre)
        params = Correlation().res_sub(params)
    elif case_id == "serve":
        params = Correlation().res_sub(params)
    elif case_id == "address_list":
        params = Correlation().res_sub(params)
    elif case_id == "change_price":
        params = Correlation().res_sub(params)
    elif case_id == "serve_order_pay":
        order_sn = pre_res_more["serve_done"]["body"]["data"]["order_sn"]
        params = Correlation().res_sub(params, order_sn)
        # 更改数据库数据
        conn = init_db("db_01")
        conn.exec("UPDATE hs_serve_order_info SET order_status=3, pay_status=1, store_id=30 WHERE order_sn={}".format(
            order_sn))
    return url, headers, cookies, params, verif_data_pre, verif_db
