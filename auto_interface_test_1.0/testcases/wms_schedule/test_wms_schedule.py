# -*-coding:utf-8-*-
# @FileName :test_wms.py
# @Time     :2022-07-27 17:36
# @Author   :Digua
import json

import pytest
from common.general_func import *
from datas.get_case import wms_case
import time


class  TestWmsSchedule:
    @pytest.mark.parametrize("case", wms_case["出库通知单"])
    def test_wms_schedule_create(self, login_system, case):
        """
        创建出库通知
        :param login_system:
        :param case:
        :return:
        """
        # 随机生成出库业务单号
        business_no = 'ck' + str(int(time.time()))

        # logger.info(get_start_sep(f"正在执行库区管理的测试，用例id为：{case.case_id} 用例标题为：{case.case_title}  "))
        # if case.case_method.lower() == "get":
        #     res = login_system.get(case.case_url)
        #     logger.info(get_setup_sep("正在发送 GET 请求"))
        #     res_json = res.json()
        #     assert judge_expect(res_json, case.case_expected, login_system, case, res)
        # elif case.case_method.lower() == "post":
        #     logger.info(get_setup_sep("正在发送POST请求"))
        #     data = json.loads(case.case_data)
        #     res = login_system.post(case.case_url, json=data)
        #     res_json = res.json()
        #     assert judge_expect(res_json, case.case_expected, login_system, case, res)
        # elif case.case_method.lower() == 'delete':
        #     logger.info(get_setup_sep("正在发送delete请求"))
        #     res = login_system.delete(case.case_url)
        #     res_json = res.json()
        #     assert judge_expect(res_json, case.case_expected, login_system, case, res)


if __name__ == '__main__':
    pytest.main()
    # a = '{"name":"测试库区","typeCode":1,"typeName":"收货暂存区","area":"10"}'
    # print(json.loads(a))