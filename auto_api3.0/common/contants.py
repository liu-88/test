# -*-coding:utf-8-*-
# @Time     :2022-09-25 22:39
# @Author   :Digua
# 此模块用于存放路径相关的常量

"""
使用的方法说明：
os.path.realpath 返回文件所在真实绝对路径（非软连）
os.path.abspath 返回文件的绝对路径
os.path.join(patha,pathb) 拼接路径
"""
import logging
import os


# 创建一个日志收集器
logger = logging.getLogger(__name__)
# 获取当前工程所在目录
projectPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 日志文件路径
logs_path = os.path.join(projectPath,"logs")
# 配置文件存放路径
conf_path = os.path.join(projectPath, "conf")
# 用例xls文件存放路径
case_data_path = os.path.join(projectPath, "data")
# 临时文件存放路径
case_temp_path = os.path.join(projectPath,"temp")
# 模板文件存放路径
case_template_path = os.path.join(case_data_path, "data_template")

if __name__ == '__main__':
    print(logs_path)
    print(conf_path)