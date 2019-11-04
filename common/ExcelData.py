from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig



"""
定义一个获取是否运行数据的公共类
"""
class Data():
    def __init__(self, testfile, sheetname):   # testfile/sheetname  可以读取yaml，也可以调用时传参
        self.reader = ExcelReader(testfile, sheetname)

    # 获取需要运行的测试数据
    def get_run_data(self):
        run_list = list()
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == "y":
                run_list.append(line)
        return run_list

if __name__ == '__main__':
    a = Data("../data/test_data.xlsx", "用户信息").get_run_data()
    print(a)
