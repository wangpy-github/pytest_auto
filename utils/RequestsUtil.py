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
            self.log.debug("发送get请求")
            r = requests.get(url, data=data, headers=headers, cookies=cookies)
        elif method == "post":
            self.log.debug("发送post请求")
            r = requests.post(url, json=json, data=data, headers=headers, cookies=cookies)
        code = r.status_code
        cookies = r.cookies
        # RequestsCookieJar 转 dict
        cookies = requests.utils.dict_from_cookiejar(cookies)
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        res = dict()
        res["code"] = code
        res["body"] = body
        res["cookies"] = cookies
        return res

    # 重构get方法
    def get(self, url, **kwargs):
        return self.request_api(url, method="get", **kwargs)

    # 重构post方法
    def post(self, url, **kwargs):
        return self.request_api(url, method="post", **kwargs)


if __name__ == '__main__':
    # res = requests_get("http://www.baidu.com")
    data = {"token":"3dcb80537e0f1104fb66a4c292b6a53cd2150283"}
    # res = requests_post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    # res = Request().get("http://www.baidu.com")
    res = Request().post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    print(res)