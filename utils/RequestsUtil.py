"""
pip3 install requests

r.status_code #响应状态
r.content #字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩
r.headers #以字典对象存储服务器响应头，若键不存在则返回None
r.json() #Requests中内置的JSON
r.url # 获取url
r.encoding # 编码格式
r.cookies # 获取cookie
r.raw #返回原始响应体
r.text #字符串方式的响应体，会自动根据响应头部的字符编码进行
r.raise_for_status() #失败请求(非200响应)抛出异常

requests参数：
    get
        params：查询字符串
    post
        data：表单数据
        json：json数据
    verify=False：避免ssl认证
"""

import requests
from utils.LogUtil import my_log

"""
get/post/put/delete方法重构
"""


class Request():
    # 初始化log方法
    def __init__(self):
        self.log = my_log("Request")

    # 定义公共方法
    def request_api(self, url, json=None, data=None, headers=None, cookies=None, method="get"):
        if method == "get":
            self.log.debug("发送get请求,URL:" + url)
            r = requests.get(url, params=data, headers=headers, cookies=cookies, verify=False)
        elif method == "post":
            self.log.debug("发送post请求,URL:" + url)
            r = requests.post(url, json=json, data=data, headers=headers, cookies=cookies, verify=False)
        elif method == "put":
            self.log.debug("发送put请求,URL:" + url)
            r = requests.put(url, json=json, data=data, headers=headers, cookies=cookies, verify=False)
        elif method == "delete":
            self.log.debug("发送delete请求,URL:" + url)
            r = requests.delete(url, json=json, data=data, headers=headers, cookies=cookies, verify=False)
        code = r.status_code
        # RequestsCookieJar 转 dict
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        try:
            body = r.json()
        except Exception as e:
            body = r.text

        total_seconds = r.elapsed.total_seconds()
        res = dict()
        res["code"] = code
        res["body"] = body
        res["cookies"] = cookies
        res["total_seconds"] = total_seconds
        return res

    # 重构get方法
    def get(self, url, **kwargs):
        return self.request_api(url, method="get", **kwargs)

    # 重构post方法
    def post(self, url, **kwargs):
        return self.request_api(url, method="post", **kwargs)

    # 重构put方法
    def put(self, url, **kwargs):
        return self.request_api(url, method="put", **kwargs)

    # 重构delete方法
    def delete(self, url, **kwargs):
        return self.request_api(url, method="delete", **kwargs)


if __name__ == '__main__':
    # res = requests_get("http://www.baidu.com")
    data = {"token": "3dcb80537e0f1104fb66a4c292b6a53cd2150283"}
    # res = requests_post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    # res = Request().get("http://www.baidu.com")
    res = Request().post("https://test.hs.wangxuekeji.com/sites/api/?url=user/info", data=data)
    print(res)
