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
    # 期望结果列表
    verif_data_pre = []
    # 1. 根据前置条件提取需要的数据，可能有多个用例都是url中有参数，提取数据逻辑不一致，进行异常捕捉
    # 2. 提取到有用的数据之后，去替换excel的数据
    if case_id == "login":
        pass
    return url, headers, cookies, params, verif_data_pre
