# -*-coding:utf-8-*-
# @Time     :2022-09-26 17:25
# @Author   :Digua
# 此模块用于创建日志工具类

class LogSe:
    def get_start_sep(information: str) -> str:
        """
        操作阶段分隔符
        :param information: 描述信息
        :return: 返回一个操作阶段分隔符
        """
        return f"{'----start----' * 6}{information}{'----start----' * 6}"

    def get_setup_sep(information: str) -> str:
        """
        操作步骤分隔符
        :param information: 描述信息
        :return: 返回一个操作步骤分隔符
        """
        return f"{' ' * 5}{'*' * 3}{information}{'-' * 3}"

    def get_end_sep(information: str) -> str:
        """
        操作步骤分隔符
        :param information: 描述信息
        :return: 返回一个操作步骤分隔符
        """
        return f"{'___end___' * 6}{information}{'___end___' * 3}"

    def get_failed_sep(case) -> str:
        """
        测试用例未通过标识分隔符
        :param information: 描述信息
        :return: 返回一个操作步骤分隔符
        """
        return f"{' ' * 5}<{'×' * 6}>  测试用例id: {case.case_id}" \
               f" {case.case_title}  未通过"

    def get_faile_info(case):
        return f"\n用例ID：{case.case_id}\n用例标题：{case.case_title}\n请求方式：{case.case_method}\n" \
               f"URL:{case.case_url}\n用例期望值：{case.case_expected}\n" \
               f"实际返回：{case.case_act_result}"

    def get_success_sep(case) -> str:
        """
        测试用例未通过标识分隔符
        :param information: 描述信息
        :return: 返回一个操作步骤分隔符
        """
        return f"{' ' * 5}<{'√' * 6}>  测试用例id: {case.case_id} 标题： {case.case_title}  通过"
    # # 日志工具类
if __name__ == '__main__':
    print(LogSe.get_start_sep("你好"))