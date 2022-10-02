# -*-coding:utf-8-*-
# @FileName :general_func.py
# @Time     :2022-07-22 9:00
# @Author   :Digua
"""
用于存放通用函数，便于调用
"""
import json
import re

from common.logUtil import *


def replace_placeholder(s: str, **kwargs) -> str:
    """
    正则匹配参考博客：https://www.cnblogs.com/CYHISTW/p/11363209.html
    用于替换文本中的${key}占位符

    :param s: 需要查找替换的目标字符串
    :param params: 需要替换的数据，按照 key=value 格式传入
    :return: 完成替换后的字符串
    """
    # 编译正则表达式，得到一个Pattern对象
    p = re.compile('\${(.*?)}')
    # 循环扫描整个字符串，找到第一个匹配项
    while re.search(p, s):
        # 返回匹配结果的第一个组（即正则表达式第一个圆括号中的内容），并赋值给key
        key = re.search(p, s).group(1)  # 1是取第一个组，0是取完整匹配
        # 遍历传入的参数，与匹配到的ke进行匹配
        if key in kwargs:
            s = re.sub(p, str(kwargs[key]), s, count=1)
        else:
            break
    return s

def format_headers(headers: str) -> dict:
    """
    格式化从谷歌浏览器中复制的请求头
    :param headers: 参数使用三个引号的字符串格式（此格式可带换行，不需要专门转义）
    :return:
    """
    headers = headers.split("\n")
    headers_res = {}
    for h in headers:
        if (h[0:1] == ": "):
            single = h[1:].split(": ")
            headers_res[single[0]] = single[1]
            headers_res = dict(headers_res, **h)
        else:
            single = h.split(": ")
            if (len(single) != 1):
                if h == "\n":
                    continue
                else:
                    headers_res[single[0]] = single[1]
    return headers_res

def judge_expect(now_dict: dict, expected_str: str , loging_system_seission, case, res) ->bool:
    logger.info(get_setup_sep("正在进行结果判断比较"))
    """
    此函数用户判断用例中的期望值，是否实现
    :param now_dict: 目标字典
    :param expected_str: 用户期望的值
    :return: 返回是否返回预期值
    """
    # 首先判断返回的状态码
    if re.match("^[4][0-9][0-9]$", str(res.status_code)):
        logger.warning(f"{' '*5}<{'×' * 6}>用例执行未通过\n期望的目标值为：{expected_str},"
                       f"\n找到的目标值为:{res.json}\n "
                       f"\n用例请求体为：{case.case_data} "
                       f"\n请求url为:{case.case_url} "
                       f"\n请求头为：{loging_system_seission.headers} "
                       f"\n请求方式为：{case.case_method}"
                       f"\n服务器返回为{res.json()}")
        logger.info(get_failed_sep(case))
        logger.info(get_end_sep(f"id: {case.case_id} 标题: {case.case_title} 测试结束"))
        return False
    # 对传入的期望值按格式解析 将期望值键值对分开来 期望值格式为：key1=value1,key2=value2
    key_value_list = expected_str.split(',')
    # 遍历解析后的键值对
    for key_value in key_value_list:
        # 将键和值分别取出，放入List方便调用
        key_value  = key_value.split('=')
        # 将json格式的特殊值转化为dict表现形式并转化为字符串格式，方便比较
        if (key_value[1] == 'null') or (key_value[1] == 'true') or (key_value[1] == "false"):
            key_value[1] = str(json.loads(key_value[1]))
        # 目标字典中是否存在对应的键值对，存在就继续比较，不存在则直接返回False
        result_list = get_dict_value(now_dict, key_value[0])
        if key_value[1] in result_list:
            continue
        else:
            logger.warning(f"{' '*5}<{'×'*6}>用例执行未通过\n期望的目标值为：{key_value},"
                           f"\n找到的目标值为:{result_list}\n "
                           f"\n用例请求体为：{case.case_data} "
                           f"\n请求url为:{case.case_url} "
                           f"\n请求头为：{loging_system_seission.headers} "
                           f"\n请求方式为：{case.case_method}"
                           f"\n服务器返回为{res.json()}")
            logger.info(get_success_sep(case))
            logger.info(
                get_end_sep(
                    f"id: {case.case_id} 标题: {case.case_title} 测试结束"))
            return False
    logger.info(get_success_sep(case))
    logger.info(get_end_sep(f"id: {case.case_id} 标题: {case.case_title} 测试结束"))
    return True

def get_dict_value(now_dict, target_key, results=None) -> [str,]:
    """
    此函数返回给定字典中目标Key,的所有值（字典嵌套字典，字典嵌套list嵌套字典）
    :param now_dict: 需要递归查找的字典
    :param target_key: 目标keys
    :param results: 返回目标key的值的列表
    :return: 返回目标key的值的列表
    """
    # 这里将默认值设为None，然后在函数里面做判断，是为了在连续调用时，未传参数的情况下，确保每
    # 次results都为空列表，以免造成数据混乱，因为python在传递对象参数时，传递的是对象的引用
    # （即内存地址），并非对象本身，直接设置默认值为空列表时，连续空参数results调用会造成非预
    # 期结果
    if results is None:
        results = []
    for key in now_dict.keys():  # 当前迭代的字典
        data = now_dict[key]  # 当前key所对应的value赋给data

        if isinstance(data, dict):  # 如果data是一个字典，就递归遍历
            get_dict_value(data, target_key, results=results)
        elif isinstance(data, list):  # 如果是一个list，就再list中查找dict，递归遍历
            for i in data:
                if isinstance(i, dict):
                    get_dict_value(i, target_key, results=results)

        if key == target_key and isinstance(data,
                                            dict) != True:  # 找到了目标key，并且它的value不是一个字典
            results.append(str(now_dict[key]))

    return results

def add(x, lst=None):
    if lst is None:
        lst = []
    if x not in lst:
        lst.append(x)

    return lst

def main_s():
    list1 = add(1)
    print(list1)

    list2 = add(2)
    print(list2)

    list3 = add(3, [11, 12, 13, 14])
    print(list3)

    list4 = add(4)
    print(list4)


if __name__ == '__main__':
    # data = json.loads('{"success":true,"errCode":null,"errMessage":null,"totalCount":3,"pageSize":10,"pageIndex":[{"typeName":"你好呀"},"nihao"],"data":[{"id":555,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区3","code":"60104","typeCode":4,"typeName":"待检区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:19:07"},'
    #                   '{"id":554,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区","code":"60103","typeCode":3,"typeName":"存储区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:18:28"},{"id":552,"warehouseId":233,"warehouseName":"o仓库","name":"测试库2","code":"60101","typeCode":1,"typeName":"收货暂存区","area":9,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:02:49"}],"notEmpty":true,"totalPages":1,"empty":false}')
    # # print(type(data))
    # # print(data.keys())
    # # data2 = json.dumps(data)
    # # print(type(data2))
    # # print(str(data2))
    # # data3 = '{"success":true,"errCode":null,"errMessage":null,"totalCount":3,"pageSize":10,"pageIndex":[{"typeName":"你好呀"},"nihao"],"data":[{"id":555,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区3","code":"60104","typeCode":4,"typeName":"待检区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:19:07"},{"id":554,"warehouseId":233,"warehouseName":"o仓库","name":"测试库区","code":"60103","typeCode":3,"typeName":"存储区","area":1,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:18:28"},{"id":552,"warehouseId":233,"warehouseName":"o仓库","name":"测试库2","code":"60101","typeCode":1,"typeName":"收货暂存区","area":9,"deleted":0,"updateBy":247,"updateName":"pp","updateTime":"2022-07-23 23:02:49"}],"notEmpty":true,"totalPages":1,"empty":false}'
    # print(judge_expect(data, "success=true,id=555,id=554,typeName=收货暂存区"))
    a = 44
    if re.match("^[4][0-9][0-9]$", str(a)):
        print("我啊哈哈")
    print(re.match("[4][0-9][0-9]]", str(a)))
    print(str(a))
    # a = a.split("\n")
    # print(redirect(a))
    # print(data2['success'])
    # print(data)
    # # # # print(data['data'])
    # value = get_dict_value(data, "success")
    # print(value)
    # print(value)
    # a = "pass"
    # print(str(a))
    # b = 'True'
    # print(eval(a))
    # print(eval(b))
    # a = "c=我好"
    # b = a.split(":")
    # # c = b[-1].split("=")
    # print(a,b)
    # print(value)
    # main_s()
    # str_ = r"${user} 我是他的爹地，${name}"
    # dict_ = {
    #     "user": '王大大',
    #     'name': '王小小'
    # }
    # # print(replace_placeholder(str_, 'user'='damao'))
    # print(replace_placeholder(s=str_, user='"王大大"', name="'王小小'"))
