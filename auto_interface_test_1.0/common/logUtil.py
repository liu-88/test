# coding=utf-8
import logging.handlers

"""
存放日志相关的工具类，由于pytest自带的日志输出工具，
只需在pytest.ini文件中进行配置，因此这里不需要使用，此模块备用
"""

# 创建一个单例日志对象，以便在其他模块调用
logger = logging.getLogger(__name__)

def get_start_sep(information: str) -> str:
    """
    操作阶段分隔符
    :param information: 描述信息
    :return: 返回一个操作阶段分隔符
    """
    return f"{'-^^-'*6}{information}{'—^^-'*6}"

def get_setup_sep(information: str) ->str:
    """
    操作步骤分隔符
    :param information: 描述信息
    :return: 返回一个操作步骤分隔符
    """
    return f"{' '*5}{'*'*3}{information}{'-'*3}"

def get_end_sep(information: str) ->str:
    """
    操作步骤分隔符
    :param information: 描述信息
    :return: 返回一个操作步骤分隔符
    """
    return f"{'_$_'*6}{information}{'_$_'*3}"

def get_failed_sep(case) ->str:
    """
    测试用例未通过标识分隔符
    :param information: 描述信息
    :return: 返回一个操作步骤分隔符
    """
    return f"{' '*5}<{'×'*6}>  测试用例id: {case.case_id} 标题 {case.case_title}  未通过"

def get_success_sep(case) ->str:
    """
    测试用例未通过标识分隔符
    :param information: 描述信息
    :return: 返回一个操作步骤分隔符
    """
    return f"{' '*5}<{'√'*6}>  测试用例id: {case.case_id} 标题： {case.case_title}  通过"
# # 日志工具类
# class Log(object):
#     def __init__(self, name=None):
#         self.logFileName = os.path.join(cf.logs_path, '{}.log'.format(time.strftime('%Y%m%d')))#获取当前时间转化为字符串，然后放在{0}里面
#         # 创建一个日志收集器
#         self.logger = logging.getLogger(name)  # 调用模块方法，实例化了一个 Logger的对象，为啥不是构造方法，我也不知道
#     def get_log(self, level, message):
#
#         # 设置logger级别
#         # 级别高低顺序：NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
#         self.logger.setLevel(logging.DEBUG)
#         # 创建一个 handler，用于写入日志文件(指定日志输出渠道)
#         fh = logging.handlers.RotatingFileHandler(self.logFileName, maxBytes=20 * 1024 * 1024, backupCount=10,
#                                                   encoding='utf-8')
#         fh.setLevel(logging.DEBUG)
#         # 再创建一个handler，用于输出到控制台
#         ch = logging.StreamHandler()
#         ch.setLevel(logging.DEBUG)
#         # 定义handler的输出格式
#         fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s'
#         formatter = logging.Formatter(fmt)
#         fh.setFormatter(formatter)
#         ch.setFormatter(formatter)
#         # 将日志输出渠道加入到日志收集器中
#         self.logger.addHandler(fh)
#         self.logger.addHandler(ch)
#         # 记录一条日志
#         if level == 'info':
#             self.logger.info(message)
#         elif level == 'debug':
#             self.logger.debug(message)
#         elif level == 'warning':
#             self.logger.warning(message)
#         elif level == 'error':
#             self.logger.error(message)
#         else:
#             self.logger.critical(message)
#         self.logger.removeHandler(ch)
#         self.logger.removeHandler(fh)
#         # 关闭打开的文件
#         fh.close()
#
#     def debug(self, message):
#         self.get_log('debug', message)
#
#     def info(self, message):
#         self.get_log('info', message)
#
#     def warning(self, message):
#         self.get_log('warning', message)
#
#     def error(self, message):
#         self.get_log('error', message)


if __name__ == '__main__':
    print("test")
    print(get_start_sep("他好好"))
    print(get_setup_sep("nihaoya"))
    # Log('test').debug('this is debug')
    # Log('hhh').error('this is error')
    # Log('hehe').info('this is info')
    # Log('lalal').error('this is error')
