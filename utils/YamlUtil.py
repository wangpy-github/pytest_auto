# coding=utf-8
import os
import yaml

"""
yaml的封装
"""


class YamlReader():
    # 初始化文件路径，判断是否存在
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在")
        self._data = None
        self._data_all = None

    # 读取单个文档并返回
    def data(self):
        if not self._data:
            with open(self.yamlf, "r", encoding="utf-8") as f:
                self._data = yaml.safe_load(f)
        return self._data

    # 读取多个文档并返回
    def data_all(self):
        if not self._data:
            with open(self.yamlf, "r", encoding="utf-8") as f:
                self._data_all = list(yaml.safe_load_all(f))  # 可迭代对象转为列表
        return self._data_all


if __name__ == '__main__':
    pass
