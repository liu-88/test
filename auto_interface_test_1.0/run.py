# -*-coding:utf-8-*-
# @FileName :run.py.py
# @Time     :2022-07-27 19:36
# @Author   :Digua


import pytest
import os

if __name__ == '__main__':
    pytest.main()
    if __name__ == "__main__":
        # 执行pytest单元测试，生成Allure报告需要的数据存在/allure-results目录
        #pytest.main()  # CASE_DIR 用例目录
        #os.system('allure generate ./allure-results -o ./allure-report --clean')
        pytest.main(["-s", "-v", "--html=./reports/pytest.html", "--alluredir=./allure"])  # allure文件生成的目录