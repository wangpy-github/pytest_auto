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

    # 获取前置测试用例的数据
    def get_case_pres(self, pres):
        """
        有前置条件的测试用例必须写在该条件用例之后
        1. 取出所有的前置条件
        2. 根据每一个前置条件查找前置条件的测试用例，返回
        """
        case_all_list = self.reader.data()
        pre_cases_list = list()
        for pre in eval(pres):
            for line in case_all_list:
                if pre in dict(line).values():
                    pre_cases_list.append(line)
        return pre_cases_list if pre_cases_list else None


if __name__ == '__main__':
    # a = Data("../data/test_data.xlsx", "用户信息").get_run_data()
    a = Data("../data/test_data.xlsx", "用户信息").get_case_pre("pet_info")
    print(a)
