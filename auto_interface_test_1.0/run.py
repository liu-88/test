# -*-coding:utf-8-*-
# @FileName :run.py.py
# @Time     :2022-07-27 19:36
# @Author   :Digua

import pytest
import os

if __name__ == '__main__':
    pytest.main()
    os.system('allure generate /var/lib/jenkins/workspace/pythonAPIallure-results/ -o /var/lib/jenkins/workspace/pythonAPI/allure-report/ --clean')