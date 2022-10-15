# -*-coding:utf-8-*-
# @Time     :2022-10-06 18:02
# @Author   :Digua
import datetime
import os
import shutil

import pytest

from common.contants import logger, logs_path
from common.logs_utill import LogSe
from test_cases.test_basic.login import login_system


#
@pytest.fixture(scope="session", autouse=True)
def auto_login_system():
    login_system()


@pytest.fixture(scope="session", autouse=True)
def backups_logs():
    """
    用于在测试完成之后备份输出的日志文件，并以时间作为新得文件名称
    :return:
    """
    # 在测试完成之后执行
    yield
    # 将当前时间的字符串格式作为文件名称
    logger.info(LogSe.get_start_sep("开始拷贝日志文件"))
    log_name = datetime.datetime.now().strftime('%Y%m%d-%H_%M_%S')
    src = os.path.join(logs_path, "log.log")
    dst = os.path.join(logs_path, log_name + ".log")
    shutil.copy(src, dst)
