import logging
import os

"""
用于存放路径相关的常量（即无论在何处引用，返回的都是同一个值）

os.path.realpath    
os.path.dirname(文件)  返回文件所在的目录
os.path.sep   文件分隔符（根据系统自定，解决不同系统的分隔符差异造成的问题）
os.path.abspath()  返回文件的绝对路径
os.path.realpath()  返回文件的真实路径（非软连接（类似于快捷方式））
"""
# 获取当前工程所在目录
projectPath = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__))
    + os.path.sep + "..")  # 返回当前文件所在目录的上级目录的绝对路径
# 日志文件存放路径
logs_path = os.path.join(projectPath, r'logs')
# datas文件存放路径
datas_path = os.path.join(projectPath, r'datas')
# 配置文件存放路径
conf_path = os.path.join(projectPath, r'conf')  # 把projectPath路径和conf拼接起来
# 用例文件存放路径
case_path = os.path.join(projectPath, r'testcases')
# 报告文件存放路径
report_path = os.path.join(projectPath, r'reports')
city_case_path = os.path.join(case_path, r'CityBuilding')
nation_case_path = os.path.join(case_path, r'NationalProperty')

if __name__ == "__main__":
    print(projectPath)
    print(logs_path)
    print(datas_path)
    print(conf_path)
    print(case_path)
    print(report_path)
    print(city_case_path)
    print(nation_case_path)
