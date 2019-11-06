#coding=utf-8
import json

a= {
    "你啊":"看看",
    "b":"f",
    "和":{
        "a":"中国",
        "v":"v"
    }
}

d = json.dumps(a, ensure_ascii=False)
print(d)
print(type(d))
