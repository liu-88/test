# -*-coding:utf-8-*-
# @Time     :2022-09-24 22:18
# @Author   :Digua
# 此方法定义用例对象,用于集成得到的测试用例数据


class Case:
    """
    用于集成测试用例数据
    """

    def __init__(self):
        # 给予默认值，以便忽略某些字段
        self.case_row_num = None    # case所在行
        self.case_test_result_col = None # case所在列
        self.case_act_result_col = None # 返回结果所在列
        self.case_id = None         # 用例编号/id
        self.case_module = None     # 用例所属模块
        self.case_title = None      # 用例标题
        self.case_method = None     # 用例请求方式
        self.case_url = None        # 用例url
        self.case_headers = None    # 接口用例请求所需请求头
        self.case_data_template = None # 用例所使用的模板
        self.case_data = None       # 用例所携带的参数
        self.case_expected = None   # 用例的预期结果
        self.case_storage_name = None  # 与用例相关的产出
        self.case_act_result = None  # 用例实际返回结果
        self.case_test_result = None # 用例测试结果True/False

