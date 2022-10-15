# -*-coding:utf-8-*-
# @Time     :2022-10-04 10:56
# @Author   :Digua
import json
import os

import ddddocr
import requests
from common.config import ReadConf
from common.contants import logger
from common.logs_utill import LogSe
from common.tools import get_wms_image_base4


def login_system():
    logger.info(LogSe.get_start_sep("开始执行登陆操作"))
    # 获取Session对象
    # 指定headers的User-Agent字段，以便模拟浏览器登录，防止服务器端浏览器访问限制
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    # logger.info(get_setup_sep("正在读取配置文件中的登录信息"))
    # 实例化配置文件读取器，用于读取配置文件
    read_config = ReadConf("test_config.ini")
    # 获取配置test.ini文件中的用户密码
    password = read_config.get_option("wms", "password")
    # 获取配置test.ini文件中的用户名
    user = read_config.get_option("wms", 'user')

    # 获取配置文件中的data信息并替换其中参数，并转化为字典格式,这里因为要转化为字典，因此在替换的时候要带上一对引号
    # s = replace_placeholder(read_config.get_option("wms", "data"),
    data = {"clientId": "erp-client", "clientSecret": "", "grantType": "password", "password": password,
            "userName": user}
    # 获取配置文件中的验证码获取url
    image_url = read_config.get_option("wms", "login_image_url")
    # 获取配置文件中的登录接口url
    login_url = read_config.get_option("wms", "login_url")
    # logger.info(get_setup_sep("获取配置文件成功"))

    # logger.info(get_setup_sep("执行登录操作"))
    # 因图片识别准确度问题，可能造成因验证码错误而登录失败，需在登录失败后进重试操作
    # 定义重试次数
    retry_num = 3
    # 更新headers中的User-Agent字段
    # 备份重试次数，以便日志输出
    # backup_retry_num = retry_num
    while retry_num >= 1:
        try:
            # 访问image_url获取验证信息
            image_rp = requests.get(image_url).json()
            # 从返回的验证码信息中获取图片信息
            base64image = get_wms_image_base4(image_rp["data"]["codeImgBase64"]
                                              )
            # 从返回的信息中获取随机码，以便与登录接口对应起来
            random_str = image_rp['data']['randomStr']
            # 实例化ocr识别器,可以选择参数old=True来切换老式的识别方式（对部分图片识别率较高）
            orc = ddddocr.DdddOcr(old=True)
            # 从图片中识别验证码
            validate_code = orc.classification(base64image)
            print(validate_code)
            # 将获取到的随机数和验证码临时添加到请求头中（临时添加：在post中添加headers参数，更新使用update方法）
            headers = {
                "randomStr": random_str,
                "code": validate_code,
                "current-warehouse-id": "233",
                "contentType": "application/json;charset=UTF-8"
            }

            # 获取登录返回信息
            login_rp = requests.post(login_url,
                                     json=data,
                                     headers=headers).json()
            # 判断登录是否成功
            if (login_rp['success'] == True) and (login_rp['errCode'] is None):
                # logger.info(get_setup_sep("登录成功"))
                # 将获得的jwt值以及接口所需必要参数更新到headers当中
                up_headers = {
                    "Authorization": login_rp['data']['jwt'],
                    "client-id": "erp-client",
                    "system-type": "2",
                    "current-warehouse-id": "233",
                    "contentType": "application/json;charset=UTF-8"
                }
                read_config.add_option("wms", "headers", json.dumps(up_headers))
                read_config.save()
                logger.info("成功登录")
                return
            # 当因为验证码错误而失败时，抛出预期异常，以便进行重试
            elif login_rp['errMessage'] == "验证码不正确！":
                logger.info("验证码错误")
                # logger.info(f"验证码错误，登录失败，服务器返回信息为：{login_rp}")
                raise ValueError("验证码错误")
            # 当因为非验证码错误而登录失败时，抛出预期外异常，以便终结程序
            else:
                logger.info("登录失败，未知错误")
                # logger.info(f"登录失败，发生未知错误，服务器返回信息为:{login_rp}")
        # 捕获预期异常，进行重试
        except ValueError as e:

            if retry_num == 1:
                # logger.info(f"已经尝试{backup_retry_num}次登录，登录失败, 强制退出")
                # 打印堆栈信息到日志
                # logger.error("报错信息为", exc_info=True)
                # # 以下为将堆栈信息以info级别日志输入
                # import traceback
                # # 得到堆栈信息的字符串形式
                # s = traceback.format_exc()
                # logger.info(f"错误信息为：{s}")
                # pytest.exit("图片识别验证码失败，登录失败，请重试")
                logger.info("图片验证码错误超过限制次数")
                raise Exception

            else:
                # logger.info(f"重试登录")
                logger.info("重新识别验证码")
                retry_num -= 1
                continue

        # 捕获非预期异常，打印日志，终结程序
        except Exception as e:
            # raise e
            # logger.error("不在预期内的错误，已抛出异常:", exc_info=True)
            # pytest.exit("登陆时发生未知错误")
            logger.error("登录出错啦！未知错误")

            # raise e
    logger.info(LogSe.get_end_sep("完成登录操作"))


# @pytest.fixture(scope="session", autouse=True)
# def rename_log():
#     """
#     用于在测试完成之后拷贝输出的日志文件，并以时间作为新的文件名以便
#     能够长期记录每次执行的存储日志
#     :return:
#     """
#     yield
#     wms_do_excel.close()
#     logger.info(get_start_sep("拷贝日志文件"))
#     # 获取测试结束时间，并格式化时间，作为当前测试日志的文件名称，便于区分
#     log_name = datetime.now().strftime('%Y%m%d-%H_%M_%S')
#     # 将输出的日志文件拷贝并重命名，防止下次执行日志被覆盖
#     logs_path = "./logs/"
#     src = os.path.join(logs_path, "log.log")
#     dst = os.path.join(logs_path, log_name + ".log")
#     # print(dict)
#     shutil.copy(src, dst)
if __name__ == '__main__':
    login_system()
