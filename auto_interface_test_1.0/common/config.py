# -*-coding:utf-8-*-
# @FileName :config.py
# @Time     :2022-07-21 9:16
# @Author   :Digua
import configparser
import os

from common import contants as cf
from common.logUtil import logger, get_start_sep

log = logger


class Read_Conf:
    # 初始化对象,并把内容加载到对象所在内存
    def __init__(self, file_name: str):
        log.info(get_start_sep(f"处理配置文件{file_name}"))
        # 表示test.ini的目录
        self.fileName = os.path.join(cf.conf_path, file_name)
        self.cfg = configparser.ConfigParser()  # 实例化这个对象
        # 内容加载到对象所在内存   读test.ini的内容
        self.cfg.read(self.fileName)

    # 取得所有的section
    def get_sections(self):
        return self.cfg.sections()

    # 取得某section下的某option的值
    def get_option(self, section: str, option: str):
        # 调get方法，通过分区里面的key读值，返回key和value
        return self.cfg.get(section, option)

    # 添加一个section
    def add_section(self, section):
        if section in self.get_sections():
            log.info(section + "已经存在")
        else:
            self.cfg.add_section(section)

    # 删除一个section
    def del_section(self, section):
        if section in self.get_sections():
            self.cfg.remove_section(section)
        else:
            log.info("section" + section + "不存在")

    # 删除option
    def del_option(self, section, option):
        try:
            self.cfg.remove_option(section, option)
        except:
            log.error("删除option:" + option + "异常")

    # 在某个section下增加一个option
    def add_option(self, section, option, value=''):
        """
        添加一个option,如果option已经存在，那么就覆盖原有的值
        :param section: 要操作的section
        :param option: 要增加/修改的option
        :param value: 需要增加/修改的option值
        :return:
        """
        try:
            self.cfg.set(section, option, value)
            log.info("section:" + section + "下添加option:" + option + "成功")
        except:
            if section not in self.cfg.sections():
                log.error("section:" + section + "不存在")
            else:
                pass

    # 保存修改后的test.ini文件
    def save(self):
        # 以读写方式打开配置文件
        fd = open(self.fileName, 'w')
        # 写入配置文件
        self.cfg.write(fd)
        # 关闭文件
        fd.close()


if __name__ == "__main__":
    conf = Read_Conf("test.ini")
    # res = conf.get_option('stage', 'pre_url')
    # print(res)

    # conf.add_section("wms")
    # # conf.del_option("wms", "user")
    # conf.add_option("wms", "data", "{'errCode': 123, 'errMessage': '验证码不正确！', 'success': False}")
    # # conf.add_option("wms", "password", "pp")
    # # conf.add_option("wms", "login_url", "https://beta-wms.zhican.com/api/v1/users/auth/token")
    # # conf.add_option("wms", "login_image_url", "https://beta-wms.zhican.com/api/v1/users/captcha/img")
    # conf.save()
    data = conf.get_option("wms", "password")
    print(data)
