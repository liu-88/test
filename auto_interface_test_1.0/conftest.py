# -*-coding:utf-8-*-
# @FileName :conftest.py
# @Time     :2022-07-20 16:02
# @Author   :Digua
import os
import shutil
from datetime import datetime

import ddddocr
import pytest
import requests

from common.config import Read_Conf
from common.contants import logs_path
from common.get_tooken_image_guide import get_wms_image_base4
from common.logUtil import logger, get_start_sep, get_setup_sep
from common.general_func import replace_placeholder


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_make_report(item, call):
#     """
#     使用钩子函数来获取测试过程中的信息
#     :param item:``````````````````````````````````````
#     :param call:
#     :return:
#     """
#     pass

@pytest.fixture(scope="session", autouse=True)
def login_system() -> (requests.Session()):
    logger.info(get_start_sep("正在执行登陆操作"))
    # 获取Session对象
    req = requests.session()
    # 指定headers的User-Agent字段，以便模拟浏览器登录，防止服务器端浏览器访问限制
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    logger.info(get_setup_sep("正在读取配置文件中的登录信息"))
    # 实例化配置文件读取器，用于读取配置文件
    read_config = Read_Conf("test.ini")
    # 获取配置test.ini文件中的用户密码
    password = read_config.get_option("wms", "password")
    # 获取配置test.ini文件中的用户名
    user = read_config.get_option("wms", 'user')
    # 获取配置test.ini文件中接口必带的参数
    client_id = read_config.get_option("wms", "headers_client-id")
    system_type = read_config.get_option("wms", "headers_system-type")
    # 获取配置文件中得当前仓库id
    current_warehouse_id = \
        read_config.get_option("wms", "headers_current-warehouse-id")
    # 获取配置文件中的data信息并替换其中参数，并转化为字典格式,这里因为要转化为字典，因此在替换的时候要带上一对引号
    # s = replace_placeholder(read_config.get_option("wms", "data"),
    #                     password=password, user=user)
    data = eval(replace_placeholder(read_config.get_option("wms", "data"),
                                    password=f"'{password}'", user=f"'{user}'")
                )
    # 获取配置文件中的验证码获取url
    image_url = read_config.get_option("wms", "login_image_url")
    # 获取配置文件中的登录接口url
    login_url = read_config.get_option("wms", "login_url")
    logger.info(get_setup_sep("获取配置文件成功"))

    logger.info(get_setup_sep("执行登录操作"))
    # 因图片识别准确度问题，可能造成因验证码错误而登录失败，需在登录失败后进重试操作
    # 定义重试次数
    retry_num = 3
    # 更新headers中的User-Agent字段
    req.headers.update(login_headers)
    # 备份重试次数，以便日志输出
    backup_retry_num = retry_num
    while retry_num >= 1:
        try:
            # 访问image_url获取验证信息
            image_rp = req.get(image_url).json()
            # 从返回的验证码信息中获取图片信息
            base64image = get_wms_image_base4(image_rp["data"]["codeImgBase64"]
                                              )
            # 从返回的信息中获取随机码，以便与登录接口对应起来
            random_str = image_rp['data']['randomStr']
            # 实例化ocr识别器,可以选择参数old=True来切换老式的识别方式（对部分图片识别率较高）
            orc = ddddocr.DdddOcr(old=True)
            # 从图片中识别验证码
            validate_code = orc.classification(base64image)
            # 将获取到的随机数和验证码临时添加到请求头中（临时添加：在post中添加headers参数，更新使用update方法）
            temp_headers = {
                "randomStr": random_str,
                "code": validate_code,
                "current-warehouse-id": current_warehouse_id
            }

            # 获取登录返回信息
            login_rp = req.post(login_url,
                                json=data,
                                headers=temp_headers).json()
            # 判断登录是否成功
            if (login_rp['success'] is True) and (login_rp['errCode'] is None):
                logger.info(get_setup_sep("登录成功"))
                # 将获得的jwt值以及接口所需必要参数更新到headers当中
                up_headers = {
                    "Authorization": login_rp['data']['jwt'],
                    "client-id": client_id,
                    "system-type": system_type,
                    "current-warehouse-id": current_warehouse_id
                }
                req.headers.update(up_headers)
                return req
            # 当因为验证码错误而失败时，抛出预期异常，以便进行重试
            elif login_rp['errMessage'] == "验证码不正确！":
                logger.info(f"验证码错误，登录失败，服务器返回信息为：{login_rp}")
                raise ValueError("登录失败")
            # 当因为非验证码错误而登录失败时，抛出预期外异常，以便终结程序
            else:
                logger.info(f"登录失败，发生未知错误，服务器返回信息为:{login_rp}")
        # 捕获预期异常，进行重试
        except ValueError:
            if retry_num == 1:
                logger.info(f"已经尝试{backup_retry_num}次登录，登录失败, 强制退出")
                # 打印堆栈信息到日志
                logger.error("报错信息为", exc_info=True)
                # # 以下为将堆栈信息以info级别日志输入
                # import traceback
                # # 得到堆栈信息的字符串形式
                # s = traceback.format_exc()
                # logger.info(f"错误信息为：{s}")
                pytest.exit("图片识别验证码失败，登录失败，请重试")
                # raise Exception
            else:
                logger.info(f"重试登录")
                retry_num -= 1
                continue

        # 捕获非预期异常，打印日志，终结程序
        except Exception as e:
            logger.error("不在预期内的错误，已抛出异常:", exc_info=True)
            pytest.exit("登陆时发生未知错误")
            raise e


@pytest.fixture(scope="session", autouse=True)
def rename_log():
    """
    用于在测试完成之后拷贝输出的日志文件，并以时间作为新的文件名以便
    能够长期记录每次执行的存储日志
    :return:
    """
    yield
    logger.info(get_start_sep("拷贝日志文件"))
    # 获取测试结束时间，并格式化时间，作为当前测试日志的文件名称，便于区分
    log_name = datetime.now().strftime('%Y%m%d-%H_%M_%S')
    # 将输出的日志文件拷贝并重命名，防止下次执行日志被覆盖
    src = os.path.join(logs_path, "log.log")
    dst = os.path.join(logs_path, log_name + ".log")
    # print(dict)
    shutil.copy(src, dst)


if __name__ == '__main__':
    # 对函数进行测试，需要注释掉夹具的装饰器！
    # a,b = login_system()
    # print(a)
    # print(b)
    rename_log()
