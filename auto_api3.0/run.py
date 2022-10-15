# -*-coding:utf-8-*-
# @Time     :2022-10-06 19:07
# @Author   :Digua
import pytest


if __name__ == '__main__':
    pytest.main(["-s", "-v", "--html=./reports/pytest.html", "--alluredir=./allure"])
