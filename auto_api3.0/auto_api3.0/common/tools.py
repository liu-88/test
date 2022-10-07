# -*-coding:utf-8-*-
# @Time     :2022-09-28 9:39
# @Author   :Digua
# 此模块用于存放各种工具形方法
import base64
import json
import os
import re
from copy import copy
from operator import itemgetter

import jsonpath

from common.contants import case_temp_path, case_template_path
from common.do_excel import DoExcel



def replace_var(s, **kwargs):
    """
    用于替换文本中 ${key} 占位符

    re模块参考博客：https://www.cnblogs.com/CYHISTW/p/11363209.html
    :param s: 需要查找替换的目标字符串
    :param kwargs: 需要替换的数据，key=value 格式
    :return: 替换后的字符串
    """
    keys = kwargs.keys()
    for i in keys:
        p = "\${"+f"{i}"+"}"
        print(p)
        s = re.sub(p,str(kwargs[i]), s)
    return s

# 将图片转化为base64编码格式并返回
def img_base64(image_path):
    """
    :param image_path: 图片路径
    :return: 返回图片对应的base64编码
    """
    with open(image_path, 'rb') as f:
        image =  f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return image_base64

# # 将图片转化为base64编码格式并携带规则返回
def img_base64_guide(image_path):
    """
        :param image_path: 图片路径
        :return: 返回图片对应的base64编码
        """
    with open(image_path, 'rb') as f:
        image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return 'data:image/jpeg;base64'+image_base64

def format_headers(data):
    """
        将下列字符串转成字典
        version: 1.0
        alias: unSet
        orgcode: 8651010000002
        token: 045FD2942C984CE5A81838F16A65A1E1
        level: undefined
        data: {"findBytitle":"","recommend":0,"pageSize":10,"pageIndex":1}
        :param data:传入实例相同的字符串
        :return:返回字典格式，可直接用于form-data传参
        """
    pass

def get_wms_image_base4(contain_image_str: str) ->str:
    """
    筛选wms系统中的验证码图片base64信息，注意这里传入的是返回信息中codeImgBase64的值，
    而不是整个返回信息
    :param contain_image_str: 包含验证码图片base64格式字符串
    :return: base64格式的图片信息
    """
    res = re.search('(.*)[,](.*)', contain_image_str)
    return res.group(2)

# 此方法已用jsonpath代替
def recu_dict_value(now_dict, target_key, results=None):
    """
    次函数返回嵌套字典中，目标Key,的所有值（可用于对返回结果的判断）
    :param now_dict: 需要递归查找的字典
    :param target_key: 目标key
    :param results: 返回目标key的值的列表
    :return: 返回目标key的值的列表
    """
    if results == None:
        results = []
    for key in now_dict.keys():
        data = now_dict[key]
        if key == target_key:
            results.append(str(now_dict[key]))
        if isinstance(data, dict): # 如果遍历到的值是一个字典，就继续递归遍历
            recu_dict_value(data, target_key, results=results)
        elif isinstance(data,list): # 如果是一个列表，也继续递归遍历
            for i in data:
                if isinstance(i,dict):
                    recu_dict_value(i, target_key, results=results)
    return results

def dis_template(case):
    # 组装模板所在路径
    template_path = os.path.join(case_template_path,case.case_data_template)
    # 获取模板
    with open(template_path,"r",encoding="utf-8") as f:
        data = json.load(f)
        if case.case_data:
            data.update(case.case_data)
    # 对模板内容进行替换
    replace_template(data)
    case.case_data = data
    return case
    # depend_field = data.get("dependent",None)
    # if depend_field:
    #     # 遍历需要依赖的字段
    #     for i in  depend_field:
    #         # 获取依赖字段的信息
    #         field_info = data.get(i)
    #         # if type(field_info) == list:
    #         # 组装依赖字段所依赖的文件路径
    #         file_path2 = os.path.join(case_temp_path,field_info.get("source"))
    #         with open(file_path2,"r",encoding="utf-8") as f:
    #             depend_file = json.load(f)
    #         # 获取需要查找判断的字段
    #         # 查找判断所需对应的源文件字段
    #         s_field = field_info.get("check_source")
    #         # 查找判断所需依据的字段
    #         j_field = field_info.get("check")
    #         # 遍历获取的依赖文件
    #         for j in depend_file:
    #             # 判断查找条件是否满足
    #             if get_keys_values(j,s_field) == get_keys_values(data,j_field):
    #                 data[i] = j[field_info["source_field"]]
    #                 if "dependent" in data:
    #                     del data["dependent"]
    #                 case.case_data=data
    # return case

def replace_template(data):
    depend_field = data.get("dependent", None)
    # 判断是否有依赖字段
    if depend_field:
        # 遍历需要依赖的字段
        for i in depend_field:
            # 获取依赖字段的信息
            field_info = data.get(i)
            if isinstance(field_info,dict):
                if field_info.get("dependent"):
                    replace_template(field_info)
                elif field_info.get("source_field",None):
                    # if type(field_info) == list:
                    # 组装依赖字段所依赖的文件路径
                    file_path2 = os.path.join(case_temp_path, field_info.get("source"))
                    with open(file_path2, "r", encoding="utf-8") as f:
                        depend_file = json.load(f)
                    # 获取需要查找判断的字段
                    # 查找判断所需对应的源文件字段
                    s_field = field_info.get("check_source")
                    # 查找判断所需依据的字段
                    j_field = field_info.get("check")
                    # 遍历获取的依赖文件
                    for j in depend_file:
                        # 判断查找条件是否满足
                        if get_keys_values(j, s_field) == get_keys_values(data,
                                                                          j_field):
                            data[i] = j[field_info["source_field"]]
                            if "dependent" in data:
                                del data["dependent"]
                            if "check" in data:
                                del data["check"]
            elif isinstance(field_info,list):
                # 遇到对应字段是list，则继续递归替换
                if field_info:
                    for i in field_info:
                        replace_template(i)

# def dis_get_depend_info(file_path, field_list, value_list):
#     with open(file_path,"r") as f:
#         depend_file = json.load(f)
#     for i in depend_file:

# 获取键列表对应的值列表
def get_keys_values(s_dict, keys):
    i = itemgetter(*keys)
    return i(s_dict)

# 对返回结果进行判断
def judge_expect(case, source_do_excel):
    expect = case.case_expected
    expect = expect.split(",")
    source_do_excel.write(case.case_row_num,
                          int(case.case_act_result_col),
                          case.case_act_result)
    act_result = json.loads(case.case_act_result)
    for i in expect:
        j = i.split("=")
        a =  jsonpath.jsonpath(act_result,f"$..{j[0]}")
        try:
            j[1] = json.loads(j[1])
        except json.decoder.JSONDecodeError:
            pass
        if j[1] in a:
            continue
        else:
            case.case_test_result = "FAIL"
            source_do_excel.write_case_result(case)
            return False
    case.case_test_result = "PASS"
    source_do_excel.write_case_result(case)
    return True


if __name__ == '__main__':
    # t = "Python中的正则表达式方面的功能，很强大其中就包括re.sub，实现正则的替换。" \
    #     "功能很强大${大王}，所${王王}以导致${大王}用法稍微有点复杂。" \
    #     "所以当${小王}遇到稍${大王}微复杂的用${大王}法时候，就容易犯错。" \
    #     "所以此处，总结${小王}一下，在使用re.sub的时候，需${小王}要注意的一些事情。"
    # t2=replace_var(t,大王="{sdlkfja;s}}", 小王="{}skl;fjajf}")
    # print(t2)
    #
    # a = [0,1,2,3,4,5,6,7,8,9]
    # print(a[0:-1:2])
    # b = {"a": 1,"b": "ss"}
    # a = ("a")
    # print(json.dumps(a, ensure_ascii=False))
    # a = "a"
    # print(json.loads(a))
    # print(fo(1))
    # print(fo(1))
    # print(b["a"])
    # data3 = '{"success":"1006", "errCode":null,"errMessage":null,"totalCount":3,"pageSize":10,"pageIndex":[{"typeName":"你好呀"},"nihao"],"data":[{"id":555,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区3","code":"60104","typeCode":4,"typeName":"待检区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:19:07"},{"id":554,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区","code":"60103","typeCode":3,"typeName":"存储区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:18:28"},{"id":552,"warehouseId":233,"warehouseName":"o仓库","name":"测试库2","code":"60101","typeCode":1,"typeName":"收货暂存区","area":9,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:02:49"}],"notEmpty":true,"totalPages":1,"empty":false}'
    # print(get_keys_values(json.loads(data3),["success","data","errCode"]))
    # print([1,2,3]==list((1,2,3)))
    # a = {'dependent': ['typeCode'], 'name': '接口测试库区', 'typeCode': {'source': 'area_type.json', 'check': ['typeName'], 'source_field': 'code'}, 'typeName': '待检区', 'area': '100'}
    # b = {'name': '接口测试收货暂存区1', 'typeName': '收货暂存区', 'area': '1'}
    # # a.update(b)
    # # print(a)
    # a = [1,2,3,8,9]
    # b = [3,9,1,1]
    # print(set(a)>set(b))
    a = {"dependent": ["entryBillSn"],"arrivalTime":"2022-10-06 10:22:02","licensePlateNo":"川A12345","vehicleType":"货车","driverName":"司机2","driverTelephone":"13122222222","deliveryBillUrl":[],"entryBillSn":{"source": "arrival_ways.json","check": ["orderType"],"check_source": ["code"],"source_field": "name"},"orderNo":"WSS","orderType":1,"orderTypeName":"销售退货",
  "warehouseId":233,
  "warehouseName":"o仓库",
  "warehouseTaskDetailsList":
  [{"dependent":["productionDate"],"productionDate":{
    "source": "arrival_ways.json",
    "check": ["stockType"],
    "check_source": ["code"],
    "source_field": "name"
  },"attribute":"2.5kg/包*10包","skuName":"测试商品","skuCode":"AAA00001","unitName":"件","unitCode":"件","urlList":[],"arriveNum":100,"arriveWeight":null,"quantityNum":100,"quantityWeight":0,"weightManage":false,"entryReceiptItemId":6973,"stockType":1,"batchNo":null}
  ]
}
    replace_template(a)
    print(a)
    # a = {
    #     "a":"b",
    #     "c":{"a":"b"}
    # }
    # def wawa(a):
    #     a["a"] = "A"
    #     ll = a.get("c",None)
    #     if ll:
    #         wawa(ll)
    #
    # wawa(a)
    # print(a)
    # print(type(a))
    # print(isinstance(a,dict))
    # data4 = json.loads(data3)
    # print(type(data4["success"]))

