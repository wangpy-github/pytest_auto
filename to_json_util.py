import json

string = """
name: admin
password: cs66888
online: s
"""


def form_data_to_json(string):
    res_list = string.strip().split("\n")
    res_dict = dict([line.strip().split(": ", 1) for line in res_list])
    json_str = json.dumps(res_dict)
    with open("./json_data.json", "w") as f:
        f.write(json_str)


form_data_to_json(string)
