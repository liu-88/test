# -*-coding:utf-8-*-
# @FileName :get_tooken_image_guide.py
# @Time     :2022-07-25 11:43
# @Author   :Digua
""""
不同系统返回的token,图片验证码base64的信息格式可能有所不同（有的会添加额外信息，需要对字符串进
行处理)，为方便读取不同系统的token和图片验证码信息，这里针对不同系统返回的信息处理，返回真正需要
的内容，每一次对接新的系统可能需要新的函数，这取决于返回数据格式
"""
import re


def get_wms_token(contain_token_str: str) -> str:
    """
    筛选返回的token 信息
    :param contain_token_str:
    :return:
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

if __name__ == '__main__':
    str = "data:image/jpeg;base64,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"

    print(get_wms_image_base4(str))
    # idex = res.span()[0]
    # print(idex)
    # print(type(idex))
    # str2 = str[idex:]
    # print(str2)