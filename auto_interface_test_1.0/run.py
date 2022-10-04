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
        pytest.main(["-q", './testcases', '--alluredir', './allure-results'])  # CASE_DIR 用例目录