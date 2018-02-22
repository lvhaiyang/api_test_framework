#!encoding=utf-8

from __future__ import unicode_literals
import sys
import platform
from lib.core import *
from lib.log import capture_log
from lib.send_mail import send_mail


def main(help_switch=None, test_data_switch=None, excel_file_path=None, mail_switch=None, mail_addrs=None, env_path=None):
    '''
    执行测试用例入口文件
    :param excel_file_name:      测试用例文件  string
    :return:    无
    '''
    if env_path is None:
        env_path = sys.path[0]

    start_date_time = create_run_time()
    start_str_time = start_date_time.strftime("%Y_%m_%d_%H_%M_%S")
    logger = capture_log(start_str_time, env_path)

    if help_switch == 1 or test_data_switch == 0:
        usage(logger)
        return

    logger.info(u'开始运行测试: ' + start_date_time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(u'测试环境：{}'.format(TEST_ENV))
    logger.info(u"测试用例文件：{}".format(excel_file_path))
    # 创建execl报告
    wb, ws = set_report_template(logger)
    # 读取excel测试用例
    test_datas = read_case_file(excel_file_path, logger)
    # 创建临时log文件
    json_file_path = create_temp_log_file(logger, env_path)
    # 执行case
    test_report = run_case(test_datas, json_file_path, logger, env_path)
    # 测试结果写入测试报告
    report_file_path = write_report(start_str_time, wb, ws, test_report, logger, env_path)
    # 生成测试信息
    stop_date_time = create_run_time()
    test_info = generate_test_info(start_date_time, stop_date_time, test_report, excel_file_path)

    # 发送邮件
    if mail_switch == 1:
        logger.info(u'发送邮件功能： 开启')
        send_mail(logger=logger, mailto_addrs=mail_addrs, test_report=test_report, test_info=test_info, report_file_path1=report_file_path,
                  report_file_path2='{0}.log'.format(report_file_path.split('.xls')[0]))
    else:
        logger.info(u'发送邮件功能： 关闭')

    logger.info(u'自动化测试结束，请查看报告')
    logger.info(u'结束时间: {}'.format(test_info['stop_log_time']))
    logger.info(u'测试用时: {}'.format(test_info['run_continue_time']))
    logger.info(u'测试环境：{}'.format(TEST_ENV))
    logger.info(u'测试用例: {}'.format(test_info['test_case_file']))
    logger.info(u'测试概要: pass: {}    fail: {}    error:  {}'.format(test_info['total_pass'], test_info['total_fail'], test_info['total_error']))
    logger.info(u'通 过 率: {}'.format(test_info['pass_rate']))



def usage(logger):
    logger.info(u'运行测试说明')
    logger.info(u'进入juzitest_framework目录')
    logger.info(u'运行 run_test.py 文件')
    logger.info(u'参数说明 -t 指定测试用例文件(必选参数)； -m 发送邮件')
    logger.info(u'例.  python run_test.py -t 基础平台测试用例.xls -m lvhaiyang@juzifenqi.com,zidongceshi@juzifenqi.com')


if __name__ == '__main__':

    import getopt

    if check_py_version() == '3.x':
        import imp
        imp.reload(sys)
    elif check_py_version() == '2.x':
        reload(sys)
        if re.match('Win', platform.system()):
            sys.setdefaultencoding('gbk')
        else:
            sys.setdefaultencoding('utf8')

    # 帮助
    help_switch = 0
    # 发送邮件
    mail_switch = 0
    mailto_addrs = None
    # 读取测试用例
    test_data_switch = 0
    excel_file_path = None

    opts, args = getopt.getopt(sys.argv[1:], 'ht:m:', ['help'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            help_switch = 1
        if opt_name in ('-t'):
            test_data_switch = 1
            excel_file_path = opt_value
        if opt_name in ('-m'):
            mail_switch = 1
            mailto_addrs = opt_value.split(',')

    main(help_switch=help_switch, test_data_switch=test_data_switch, excel_file_path=excel_file_path, mail_switch=mail_switch, mail_addrs=mailto_addrs)
