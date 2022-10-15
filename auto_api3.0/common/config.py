# -*-coding:utf-8-*-
# @Time     :2022-09-25 22:34
# @Author   :Digua
# 此方法用于读写配置文件
import configparser
import os

from common import contants


class ReadConf:
    # 初始化对象，并把内容加载到对象所在内存
    def __init__(self, file_name="test_config.ini"):
        """
        :param file_name: 配置文件名称
        """
        # 组装配置文件路径
        self.file_name = os.path.join(contants.conf_path, file_name)
        # 实例化ConfigParser对象
        self.cfg = configparser.ConfigParser()
        # 加载目标配置文件
        self.cfg.read(self.file_name)

    # 获取配置文件中的所有节点
    def get_sections(self):
        return self.cfg.sections()

    # 获取指定节点的配置信息，并以字典形式返回
    def get_section_conf(self, section_name):
        return dict(self.cfg.items(section_name))

    # 获取指定节点指定项的值
    def get_option(self, section_name="wms", option_name="user"):
        """
        :param option_name:  项名称
        :param section_name:  节点名称
        :return:
        """
        return self.cfg.get(section_name, option_name)

    # 添加一个节点
    def add_section(self, section_name="wms"):
        if section_name in self.get_sections():
            pass
        else:
            self.cfg.add_section(section_name)

    # 删除一个节点
    def del_section(self, section_name):
        if section_name in self.get_sections():
            self.cfg.remove_section(section_name)
        else:
            pass

    # 添加一个项
    def add_option(self, section_name, option_name, option_value):
        """
        :param section_name: 节点名称
        :param option_name:  项名称
        :param option_value: 项的值
        :return:
        """
        try:
            self.cfg.set(section_name, option_name, option_value)
        except Exception as e:
            raise e
            # print("添加出错二")
            # if section_name not in self.cfg.sections():
            #     print("这个选项没有哦")
            #     pass
            # else:
            #     pass

    # def set_option(self,section_name, option_name, option_value):
    #     try:
    #         self.cfg.set

    # 删除一个项
    def del_option(self,section_name,option_name):
        if section_name in self.cfg.sections():
            self.cfg.remove_option(section_name, option_name)
        else:
            pass
    # 保存修改后的配置文件
    def save(self):
        cff = open(self.file_name, 'w')
        self.cfg.write(cff)
        cff.close()

if __name__ == '__main__':
    conf = ReadConf("test_config.ini")
    # conf.add_option("wms", "user", "pp")
    # conf.add_option("wms", "password","L6D5K6")
    # conf.add_option("wms","base_url",
    #                 "https://beta-wms.zhican.com")
    # conf.add_option("wms","login_url",
    #                 "https://beta-wms.zhican.com/api/v1/users/auth/token")
    # conf.add_option("wms","login_image_url",
    #                 "https://beta-wms.zhican.com/api/v1/users/captcha/img")
    # conf.add_option("wms","case_id", "1")
    # conf.add_option("wms","case_title", "2")
    # conf.add_option("wms","case_url", "3")
    # conf.add_option("wms","case_headers", "4")
    # conf.add_option("wms","case_data", "5")
    # conf.add_option("wms","case_method", "6")
    # conf.add_option("wms","case_expected", "7")
    # print(conf.get_sections())
    # print(conf.get_section_conf("wms")["case_id"])
    print(conf.get_option("wms","password"))

    # conf.save()