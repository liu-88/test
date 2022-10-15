# -*-coding:utf-8-*-
# @Time     :2022-10-04 22:18
# @Author   :Digua
import json
import os

import pytest
import requests

from common.config import ReadConf
from common.contants import case_template_path, case_temp_path, logger
from common.do_excel import DoExcel
from common.logs_utill import LogSe
from common.tools import dis_template, judge_expect

# 从文件读取case
get_data = DoExcel("wms_case.xlsx", "库区管理", "wms")
get_case = get_data.read_case()
# 获取配置文件读取器
conf = ReadConf()


# 获取请求所用header

class TestArea:

    @pytest.mark.parametrize("case", get_case)
    def test_create_area(self, case):
        get_header = json.loads(conf.get_option(option_name="headers"))
        logger.info(LogSe.get_start_sep(case.case_title))
        # 组合请求接口路径
        url = conf.get_option("wms", "base_url") + case.case_url
        # 判断是否有data模板，有模板则先处理模板,并放回处理后的data
        if case.case_data_template:
            case = dis_template(case)
        # 判断请求方式
        if case.case_method.lower() == "post":
            # 发送post请求
            re = requests.post(url, json=case.case_data, headers=get_header)
            # 获取字符串格式返回结果
            re_data_str = re.text
            # 获取字典格式返回结果
            re_data_dict = re.json()
            # 将用例的返回结果的字符串格式记录到case中
            case.case_act_result = re_data_str
            # 判断用例是成功通过，并将测试结果写入excel
            result = judge_expect(case, get_data)
            if result == False:
                logger.warning(LogSe.get_faile_info(case))
                logger.info(LogSe.get_end_sep(case.case_title))
            else:
                logger.info(LogSe.get_success_sep(case))
                logger.info(LogSe.get_end_sep(case.case_title))
            # 判断是否需要存储得到的数据（返回数据中必须有 data 字段）
            if case.case_storage_name:
                # 用例执行成功才保存正确结果
                if result == True:
                    # 取出要保存的数据
                    st_data = re_data_dict["data"]
                    with open(os.path.join(case_temp_path,
                                           case.case_storage_name), "w",
                              encoding="utf-8") as f:
                        json.dump(st_data, f, ensure_ascii=False)
            assert result
        elif case.case_method.lower() == "get":
            # 发送get请求
            re = requests.get(url, params=case.case_data, headers=get_header)
            # 获取字符串格式返回结果
            re_data_str = re.text
            # 获取字典格式返回结果
            re_data_dict = re.json()
            # 将用例的返回结果的字符串格式记录到case中
            case.case_act_result = re_data_str
            # 判断用例是成功通过，并将测试结果写入excel
            result = judge_expect(case, get_data)
            if result == False:
                logger.warning(LogSe.get_faile_info(case))
                logger.info(LogSe.get_end_sep(case.case_title))
            else:
                logger.info(LogSe.get_success_sep(case))
                logger.info(LogSe.get_end_sep(case.case_title))
            # 判断是否需要存储得到的数据（返回数据中必须有 data 字段）
            if case.case_storage_name:
                # 用例执行成功才保存正确结果
                if result == True:
                    # 取出要保存的数据
                    st_data = re_data_dict["data"]
                    with open(os.path.join(case_temp_path,
                                           case.case_storage_name), "w",
                              encoding="utf-8") as f:
                        json.dump(st_data, f, ensure_ascii=False)
            assert result


if __name__ == '__main__':
    pytest.main(["./test_create_area.py", "-vs"])
    # data8 ={
    #     "receiptId":2305
    # }
    # re = requests.get("https://beta-wms.zhican.com/api/v1/warehouse/entry/receipt/detail",
    #              params=data8,headers=get_header)
    # print(re.json())
