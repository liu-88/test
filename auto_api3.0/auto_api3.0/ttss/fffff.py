# -*-coding:utf-8-*-
# @Time     :2022-09-25 23:02
# @Author   :Digua
# from common import contants
#
# print(contants.projectPath)
# print(contants.logs_path)
import json
from common.tools import replace_template

with open("./tessssss.json","r",encoding="utf-8") as f:
    a = json.load(f)
print(a)
replace_template(a)
print(a)

with open("./teesss.json","w",encoding="utf-8") as f:
    json.dump(a,f,ensure_ascii=False)