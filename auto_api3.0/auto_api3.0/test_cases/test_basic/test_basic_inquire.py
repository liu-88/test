# -*-coding:utf-8-*-
# @Time     :2022-10-04 10:31
# @Author   :Digua
import json
import os

import pytest
import requests

from common.config import ReadConf
from common.contants import case_temp_path, logger
from common.do_excel import DoExcel
from common.logs_utill import LogSe
from common.tools import judge_expect

get_data = DoExcel("wms_case.xlsx","基础查询")
get_case = get_data.read_case()
conf = ReadConf("test_config.ini")
class TestBasicInquire:
    @pytest.mark.parametrize("case", get_case)
    def test_inquire_type(self, case):
        get_header = conf.get_option("wms", "headers")
        logger.info(LogSe.get_start_sep(case.case_title))
        url = conf.get_option("wms", "base_url") + case.case_url
        re = requests.get(url,headers=json.loads(get_header))

        re_data_str = re.text
        re_data_dict = re.json()
        case.case_act_result = re_data_str
        # 如果成功获取，将成功的结果存入Json文件
        result = judge_expect(case, get_data)
        # 如果用例成功返回结果，便将返回结果的data数据保存下载
        if result == True:
            re2_data = re_data_dict["data"]
            with open(os.path.join(case_temp_path,case.case_storage_name),"w",encoding="utf-8") as f:
                json.dump(re2_data,f,ensure_ascii=False)
            logger.info(LogSe.get_success_sep(case))
        else:
            logger.warning(LogSe.get_faile_info(case))
            logger.info(LogSe.get_end_sep(case.case_title))
        assert result

if __name__ == '__main__':
    # TestBasicInquire().test_inquire_type(get_case[0])
    # a = ["'1'", "true"]
    # print(json.loads(a[1]),type(json.loads(a[0])))
    pytest.main(["./test_basic_inquire.py","-vs"])