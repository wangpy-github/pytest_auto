# coding=utf-8
import re

string = """
ticket: abc
categoryId: 你好
orderBy: new-desc
type: 1
"""


def form_data_to_json(string):
    res_list = string.strip().split("\n")
    res_dict = dict([line.strip().split(": ", 1) for line in res_list])
    # json_str = json.dumps(res_dict)   # 汉字会编码
    res_str = str(res_dict)
    json_str = re.sub("'", '"', res_str)
    with open("./json_data.json", "w") as f:
        f.write(json_str)


form_data_to_json(string)
