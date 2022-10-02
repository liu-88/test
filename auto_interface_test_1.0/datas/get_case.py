# -*-coding:utf-8-*-
# @FileName :get_case.py
# @Time     :2022-07-28 22:44
# @Author   :Digua
"""
用于存放获取测试用例数据
"""
from common.do_excel import DoExcel

wms_case = {}
wms_case["库区管理"] = DoExcel("wms_case.xlsx", "库区管理", "wms").read
wms_case["出库通知单"] = DoExcel("wms_schedule.xlsx", "出库通知单", "wms").read