import requests
from utils.LogUtil import my_log

# get 方法的封装
# def requests_get(url, headers=None, data=None, **kwargs):
#     r = requests.get(url, headers=headers, data=data)
#     code = r.status_code
#     try:
#         body = r.json()
#     except Exception as e:
#         body = r.text
#     res = dict()
#     res["code"] = code
#     res["body"] = body
#     return res


# post 方法的封装
# def requests_post(url, headers=None, json=None, data=None, **kwargs):
#     r = requests.post(url, json=json, headers=headers, data=data)
#     code = r.status_code
#     try:
#         body = r.json()
#     except Exception as e:
#         body = r.text
#     res = dict()
#     res["code"] = code
#     res["body"] = body
#     return res


"""
get/post方法重构
"""


class Request():
    # 初始化log方法
    def __init__(self):
        self.log = my_log("Request")
    # 定义公共方法
    def request_api(self, url, json=None, data=None, headers=None, cookies=None, method="get"):
        if method == "get":
            self.log.debug("发生get请求")
            r = requests.get(url, data=data, headers=headers, cookies=cookies)
        elif method == "post":
            self.log.debug("发生post请求")
            r = requests.post(url, json=json, data=data, headers=headers, cookies=cookies)
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        res = dict()
        res["code"] = code
        res["body"] = body
        return res

    # 重构get方法
    def get(self, url, **kwargs):
        return self.request_api(url, method="get", **kwargs)

    # 重构post方法
    def post(self, url, **kwargs):
        return self.request_api(url, method="post", **kwargs)


if __name__ == '__main__':
    # res = requests_get("http://www.baidu.com")
    data = {
        "json": '{"token": "3933241097da4ef47c9f8e7458dfd5624d116237"}'
    }
    # res = requests_post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    # res = Request().get("http://www.baidu.com")
    res = Request().post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    print(res)
