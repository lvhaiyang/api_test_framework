#!encoding=utf-8

from __future__ import unicode_literals
import xlrd
import xlwt
import json
import re
import os
import sys
import datetime
import requests
import traceback
import platform
from importlib import import_module
from config import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def save_json_file(json_file_path, data):
    '''
    保存json格式文件
    :param json_file_path:  文件路径
    :param data: 文件内容    字典格式
    :return: 无
    '''
    # print 'START RUN: save_json_file()'
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(data))


def load_json_file(json_file_path):
    '''
    读取json文件
    :param json_file_path: 文件路径
    :return: 文件内容    字典格式
    '''
    # print 'START RUN: load_json_file()'
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        return data


def analysisExcelFile(filePath):
    '''
    解析 Excel 文件
    :param filePath: Excel 文件路径
    :return: 测试用例数据列表 每个元素是一个字典
    '''
    # logger.info(u'开始解析 Excel 文件')
    data = xlrd.open_workbook(filePath)
    table = data.sheets()[0]
    nrows = table.nrows
    data = []
    for i in range(0, nrows):
        row = table.row_values(i)
        # print row
        data.append(row)

    return data


def set_excel_style(colour_index=1):
    '''
    excel 样式模板
    :param colour_index:  单元格背景颜色
    :return:  单元格样式
    '''
    # print 'START RUN: set_excel_style()'
    style = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式

    pattern = xlwt.Pattern()                 # 创建一个模式
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN     # 设置其模式为实型
    pattern.pattern_fore_colour = colour_index     # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,  the list goes on...
    style.pattern = pattern             # 将赋值好的模式参数导入Style

    fnt = xlwt.Font()                        # 创建一个文本格式，包括字体、字号和颜色样式特性
    fnt.name = u'微软雅黑'                # 设置其字体为微软雅黑
    fnt.bold = True
    style.font = fnt                    #将赋值好的模式参数导入Style

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders         #将赋值好的模式参数导入Style

    return style


def request_mode(session=None, request_type=None, url=None, data_type=None, data=None, headers=None, logger=None):
    '''
    运行接口测试模块
    :param session:      requests session 对象
    :param request_type:     请求类型  post  get
    :param url:         请求url
    :param data_type:     请求参数类型
    :param data:     请求参数
    :param headers:      请求headers
    :param logger:      logging 日志对象
    :return:     requests 请求成功返回response对象， 请求失败返回错误类型
    '''

    logger.debug(u'开始请求接口：{0}'.format(url))
    headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1'
    try:
        if request_type == u'post':
            if data_type == u'json':
                res = session.post(url=url, json=data, headers=headers, verify=False, timeout=60)
            else:
                res = session.post(url=url, data=data, headers=headers, verify=False, timeout=60)
        elif request_type == u'get':
            res = session.get(url=url, params=data, headers=headers, verify=False, timeout=60)
        else:
            logger.debug(u'请求类型错误')

        logger.debug(u'响应状态码为：{}'.format(res.status_code))
        return res

    except requests.exceptions.ReadTimeout as e:
        logger.debug(traceback.format_exc())
        return 'ReadTimeout'
    except requests.exceptions.ConnectionError as e:
        logger.debug(traceback.format_exc())
        return 'ConnectionError'
    except Exception as e:
        logger.debug(traceback.format_exc())
        # logger.debug(u'接口 ： {}  测试出错  '.format(url))
        return None


def verify_mode(res, expect_data=None, logger=None):
    '''
    验证测试用例
    :param res:      request_mode 方法返回值
    :param expect_data:     预期结果
    :param logger:       logging 日志对象
    :return:    request_mode 方法返回值， 接口状态码或者错误信息， 测试结果
    '''

    logger.info(u'开始验证测试结果')

    if res is None:
        logger.debug(u'接口请求错误  ！！！！！！！！！！')
        return None, u'接口请求错误', u'error'
    elif res == 'ReadTimeout':
        logger.debug(u'接口请求超时(60s)  ！！！！！！！！！！')
        return None, u'接口请求超时(60s)', u'error'
    elif res == 'ConnectionError':
        logger.debug(u'接口连接错误  ！！！！！！！！！！')
        return None, u'接口连接错误', u'error'

    # res_data = res.content
    res_data = {}
    try:
        res_data = res.json()
        # if check_py_version() == '2.x':
        #     logger.debug(u'响应结果为：{}'.format(json.dumps(res_data, ensure_ascii=False, encoding='UTF-8')))
        # elif check_py_version() == '3.x':
        #     logger.debug(u'响应结果为：{}'.format(json.dumps(res_data, ensure_ascii=False)))
    except:
        # logger.debug(traceback.format_exc())
        logger.debug(u'未发现json返回值  ！！！！！！！！！！')

    status_code = res.status_code
    if status_code != 200:
        logger.debug(u'状态码验证：失败， 状态码为 {0}  ！！！！！！！！！！'.format(status_code))
        logger.debug(u'接口 ： {}  测试出错  ！！！！！！！！！！'.format(res.url))
        return res, status_code, u'fail'
    else:
        result = ''
        if check_py_version() == '2.x':
            logger.debug(u'预期结果为 {0}'.format(json.dumps(expect_data, ensure_ascii=False, encoding='UTF-8')))
            logger.debug(u'响应结果为 {0}'.format(json.dumps(res_data, ensure_ascii=False, encoding='UTF-8')))
        elif check_py_version() == '3.x':
            logger.debug(u'预期结果为 {0}'.format(json.dumps(expect_data, ensure_ascii=False)))
            logger.debug(u'响应结果为 {0}'.format(json.dumps(res_data, ensure_ascii=False)))

        if expect_data != res_data:
            logger.debug(u'测试结果验证：失败， 预期结果与实际结果不符  ！！！！！！！！！！')
            logger.debug(u'接口 ： {}  测试未通过'.format(res.url))
            result = u'fail'
        else:
            logger.debug(u'测试结果验证：通过， 预期结果与实际结果一致')
            logger.debug(u'接口 ： {}  测试通过'.format(res.url))
            result = u'pass'

        return res, status_code, result


def set_report_template(logger):
    '''
    设置excel报告样式
    :param logger:       logging 日志对象
    :return:        xlwt workbook对象， sheet对象
    '''
    logger.info(u'开始初始化测试报告样式')
    # 定义报告样式
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("report")
    for i in [0]:
        first_col = ws.col(i)  # xlwt中是行和列都是从0开始计算的
        first_col.width = 256 * 30

    # for i in [10]:
    #     first_col = ws.col(i)  # xlwt中是行和列都是从0开始计算的
    #     first_col.width = 156 * 20

    for i in [16]:
        first_col = ws.col(i)  # xlwt中是行和列都是从0开始计算的
        first_col.width = 156 * 25

    logger.info(u'初始化测试报告样式完成')
    return wb, ws


def read_case_file(excel_file, logger):
    '''
    读取测试用例
    :param excel_file:  excel测试用例文件路径
    :param logger:        logging 日志对象
    :return:    None
    '''
    logger.info(u'开始读取测试用例 ：{0}'.format(excel_file))
    # 读取测试用例文件
    try:
        test_datas = analysisExcelFile(excel_file)
        logger.info(u'测试用例 ：{0} 读取成功'.format(excel_file))
        return test_datas
    except:
        logger.info(u'测试用例 ：{0} 读取失败！！！！！！！！！！'.format(excel_file))
        logger.info(u'请确认excel测试用例路径是否正确！！！！！！！！！！')
        return '测试用例读取失败'


def create_temp_log_file(logger, env_path):
    '''
    创建临时json文件，保存接口响应结果
    :param logger:       logging 日志对象
    :return:  json文件路径
    '''
    logger.info(u'创建临时log文件 temp_log.json')
    # 创建临时log文件
    json_file_path = os.path.join(env_path, u'test_report', u'temp_log.json')
    f = open(json_file_path, 'w')
    f.write('{}')
    f.close()

    return json_file_path


def create_run_time():
    '''
    初始化测试执行时间
    :return:  datatime格式  时间
    '''
    test_datetime = datetime.datetime.now()
    return test_datetime
    # test_date = test_datetime.date()
    # test_time = test_datetime.time()
    # run_time = u"%02d_%02d_%02d_%02d_%02d_%02d" % (
    #     test_date.year, test_date.month, test_date.day,
    #     test_time.hour, test_time.minute, test_time.second)
    #
    # current_time = u"%02d年%02d月%02d日  %02d时%02d分%02d秒" % (
    #     test_date.year, test_date.month, test_date.day,
    #     test_time.hour, test_time.minute, test_time.second)
    #
    # return run_time, current_time, test_datetime


def save_report(run_time, wb, logger, env_path):
    '''
    保存测试报告
    :param run_time:     datatime格式  时间
    :param wb:      xlwt  workboot对象
    :param logger:       logging 日志对象
    :return:    测试报告保存路径
    '''
    logger.info(u'开始保存测试报告')
    report_path = os.path.join(env_path, u'test_report')
    report_file = u'report{}.xls'.format(run_time)
    report = os.path.join(report_path, report_file)
    wb.save(report)
    logger.info(u'保存测试报告路径为 {0}'.format(report))
    return report


def write_report(run_time, wb, ws, test_report, logger, env_path):
    '''
    测试结果写入报告
    :param run_time:      datatime格式  时间
    :param wb:       xlwt  workboot对象
    :param ws:       xlwt  sheet对象
    :param test_report:     run_case方法 返回的 测试结果
    :param logger:        logging 日志对象
    :return:    save_report(run_time, wb, logger)
    '''
    logger.info(u'\n\n' + u'='*200)
    logger.info(u'测试结果写入报告')
    base_style = set_excel_style()
    style_pass = set_excel_style(3)
    style_fail = set_excel_style(2)
    style_error = set_excel_style(6)
    # 执行结果写入报告
    result_no = -2
    db_result_no = -1
    for row in range(len(test_report)):
        test_data = test_report[row]

        for k in range(len(test_data)):
            if len(test_data[k]) > 5000:
                test_data[k] = test_data[k][:5000] + '...'

        if test_data[result_no] == u'pass' and test_data[db_result_no] in [u'pass', u'未开启数据库校验']:
            for k in range(len(test_data)):
                ws.write(row, k, test_data[k], style_pass)
        elif test_data[result_no] == u'fail' or test_data[db_result_no] in [u'fail']:
            for k in range(len(test_data)):
                ws.write(row, k, test_data[k], style_fail)
        elif test_data[result_no] == u'error' or test_data[db_result_no] in [u'error']:
            for k in range(len(test_data)):
                ws.write(row, k, test_data[k], style_error)
        else:
            for k in range(len(test_data)):
                ws.write(row, k, test_data[k], base_style)

    logger.info(u'测试结果写入报告完成')
    return save_report(run_time, wb, logger, env_path)


def run_case(test_datas, json_file_path, logger, env_path):
    '''
    执行测试方法
    :param test_datas:  read_case_file方法返回值， excel测试用例 字典格式
    :param json_file_path:  create_temp_log_file方法返回值， json文件路径
    :param logger:        logging 日志对象
    :return:    列表格式  测试报告
    '''
    logger.info(u'开始运行测试用例')
    test_report = []
    logger.info(u'初始化session 执行测试用例')
    session = requests.session()
    for i in range(len(test_datas)):
        res_content = u'no response'
        test_data = test_datas[i]

        try:
            case_name, api_name, api_url, headers, request_type, data_type, data, db_switch, expect_data = test_data
        except Exception as e:
            logger.info(u'测试用例读取失败')
            return '测试用例读取失败'

        if i == 0:
            value = u'响应结果'
            value2 = u'响应时间(s)'
            value3 = u'状态码'
            value4 = u'测试结果'
            value5 = u'数据库校验结果'
            test_data.append(value)
            test_data.append(value2)
            test_data.append(value3)
            test_data.append(value4)
            test_data.append(value5)
        else:
            logger.info(u'\n\n' + u'-'*200)
            logger.info(u'开始执行第 {0} 条测试用例 ：{1}'.format(i, api_name))
            try:
                headers = json.loads(headers)
            except:
                logger.debug(u'测试用例 headers 中 json 数据转换失败！！！！！！！！！！')

            try:
                data = json.loads(data)
            except:
                logger.debug(u'测试用例 请求参数 中 json 数据转换失败！！！！！！！！！！')

            try:
                expect_data = json.loads(expect_data)
            except:
                logger.debug(u'测试用例 预期结果 中 json 数据转换失败！！！！！！！！！！')

            api_url_suffix = None
            func_name_str_cource = api_url.replace(r'/', r'_')[1:]
            func_name_str = func_name_str_cource.split('.')[0]
            try:
                api_url_suffix = func_name_str_cource.split('.')[1]
                logger.debug(u'接口中存在文件后缀名，获取成功 {0}'.format(api_url_suffix))
            except:
                logger.debug(u'接口中不存在文件后缀')

            try:
                mode_path = ''
                for case_path in os.walk(env_path):
                    for case_file in case_path[2]:
                        if re.match(func_name_str, case_file):
                            if re.match('Win', platform.system()):
                                mode_path = '.'.join(case_path[0].split('\\')[1:])
                            else:
                                mode_path = '.'.join(case_path[0].split('/')[1:])

                mode_path = 'test_api' + mode_path.split('test_api')[1]
                mode_path = mode_path.split('.__pycache__')[0]
                mode_name = u'{0}.{1}'.format(mode_path, func_name_str)
                logger.debug(u'测试用例路径 {0}'.format(mode_name))
                config_mode_path = u'.'.join(mode_name.split('.')[:2])
                config_mode_name = u'{0}.{1}_config'.format(config_mode_path, TEST_ENV)
                logger.debug(u'配置文件为 {0}'.format(config_mode_name))

                case_mode = import_module(mode_name)
                config_mode = import_module(config_mode_name)
                base_url = config_mode.BASE_URL

            except Exception as e:
                logger.debug(traceback.format_exc())
                logger.debug(u'接口 {0} 测试用例模块导入失败，配置文件导入失败  ！！！！！！！！！！'.format(api_url))

            logger.debug(u'开始测试接口   {}'.format(api_url))

            db_check_result = u'未开启数据库校验'
            # 初始化数据库
            if eval(db_setup_del) or eval(db_setup_insert):
                logger.debug(u'数据库初始化： 开启')
                try:
                    DB = case_mode.DatabaseCheck(config_mode, logger=logger, send_data=data, json_file_path=json_file_path, db_setup_del=db_setup_del, db_setup_insert=db_setup_insert, db_teardown=db_teardown, db_verify=db_verify, db_expect=db_expect)
                except:
                    logger.debug(traceback.format_exc())
                    logger.debug(u'数据库连接： 失败！！！！！！！！！！')
                else:
                    DB.run_set_up()
            else:
                logger.debug(u'数据库初始化： 关闭')

            # 接口请求
            try:
                API = case_mode.ApiTest(base_url=base_url, session=session, json_file_path=json_file_path, request_type=request_type, send_data_type=data_type, send_data=data, headers=headers, expect_data=expect_data, api_url_suffix=api_url_suffix, logger=logger)
            except:
                logger.debug(traceback.format_exc())
                logger.debug(u'自动化库中没有对应接口 {}  ！！！！！！！！！！'.format(api_url))
                res, status_code, result, response_time = u'error', None, u'error', None
            else:
                try:
                    res, status_code, result, response_time = API.run()
                    new_headers, new_send_data, new_expect_data = API.replace_data()
                    if check_py_version() == '2.x':
                        test_data[2] = json.dumps(new_headers, ensure_ascii=False, encoding='UTF-8')
                        test_data[5] = json.dumps(new_send_data, ensure_ascii=False, encoding='UTF-8')
                        test_data[11] = json.dumps(new_expect_data, ensure_ascii=False, encoding='UTF-8')
                    elif check_py_version() == '3.x':
                        test_data[2] = json.dumps(new_headers, ensure_ascii=False)
                        test_data[5] = json.dumps(new_send_data, ensure_ascii=False)
                        test_data[11] = json.dumps(new_expect_data, ensure_ascii=False)
                except:
                    # logger.debug(traceback.format_exc())
                    print(traceback.format_exc())
                    logger.debug(u'接口地址 {0}{1} 请求失败  ！！！！！！！！！！'.format(base_url, api_url))
                    res, status_code, result, response_time = None, None, u'error', None

            # 数据库校验
            if eval(db_verify) and eval(db_expect):
                logger.debug(u'数据库校验： 开启')
                try:
                    DB = case_mode.DatabaseCheck(config_mode, logger=logger, send_data=data, json_file_path=json_file_path, db_setup_del=db_setup_del, db_setup_insert=db_setup_insert, db_teardown=db_teardown, db_verify=db_verify, db_expect=db_expect)
                except:
                    logger.debug(traceback.format_exc())
                    logger.debug(u'数据库连接： 失败！！！！！！！！！！')
                    db_check_result = u'error'
                else:
                    db_check_result = DB.run_verify()
            else:
                logger.debug(u'数据库校验： 关闭')

            # 数据库测试数据清理
            if eval(db_teardown):
                logger.debug(u'数据库测试数据清理： 开启')
                try:
                    DB = case_mode.DatabaseCheck(config_mode, logger=logger, send_data=data,
                                                 json_file_path=json_file_path, db_setup_del=db_setup_del,
                                                 db_setup_insert=db_setup_insert, db_teardown=db_teardown,
                                                 db_verify=db_verify, db_expect=db_expect)
                except:
                    logger.debug(traceback.format_exc())
                    logger.debug(u'数据库连接： 失败！！！！！！！！！！')
                else:
                    DB.run_teardown()
            else:
                logger.debug(u'数据库测试数据清理： 关闭')

            # 生成报告
            if res is None:
                if status_code is None:
                    json_data = {u'接口地址 {0}{1} 请求失败'.format(base_url, api_url): ''}
                    res_content = u'接口地址 {0}{1} 请求失败'.format(base_url, api_url)
                    status_code = u'无'
                else:
                    json_data = {u'no response': ''}
            elif res == u'error':
                json_data = {u'自动化库中没有对应接口 {}'.format(api_url): ''}
                res_content = u'自动化库中没有对应接口 {}'.format(api_url)
                status_code = u'无'
            else:
                # res_content = res.content
                json_data = {}
                try:
                    json_data = res.json()
                except:
                    # logger.debug(traceback.format_exc())
                    logger.debug(u'未发现json返回值 ！！！！！！！！！！')

            try:
                if check_py_version() == '2.x':
                    test_data.append(json.dumps(res.json(), ensure_ascii=False, encoding='UTF-8'))
                elif check_py_version() == '3.x':
                    test_data.append(json.dumps(res.json(), ensure_ascii=False))
            except:
                test_data.append(res_content)

            test_data.append(u'{}'.format(response_time))
            test_data.append(u'{}'.format(status_code))
            test_data.append(u'{}'.format(result))
            test_data.append(u'{}'.format(db_check_result))

        test_report.append(test_data)

    return test_report


def check_py_version():
    '''
    检查运行环境 py2 or py3
    :return:  python 版本
    '''
    if re.match('2', sys.version):
        return '2.x'
    elif re.match('3', sys.version):
        return '3.x'
    else:
        return None


def generate_test_info(start_time, stop_time, test_report, test_case_file):
    '''
    生成测试信息
    :return: 字典 测试信息
    '''
    # 生成测试结果统计信息
    result_no = -2
    db_result_no = -1
    total_pass = 0
    total_fail = 0
    total_error = 0
    for test_data in test_report:
        if test_data[result_no] == u'pass' and test_data[db_result_no] in [u'pass', u'未开启数据库校验']:
            total_pass = total_pass + 1
        elif test_data[result_no] == u'fail' or test_data[db_result_no] in [u'fail']:
            total_fail = total_fail + 1
        elif test_data[result_no] == u'error' or test_data[db_result_no] in [u'error']:
            total_error = total_error + 1

    total_case = total_pass + total_fail + total_error
    pass_rate = float(total_pass)/total_case
    pass_rate = u'%.2f' % (pass_rate*100)
    pass_rate = u'{}%'.format(pass_rate)

    # 生成测试环境信息
    test_env = TEST_ENV

    # 生成运行时间信息
    start_log_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    stop_log_time = stop_time.strftime("%Y-%m-%d %H:%M:%S")
    run_continue_time = str(stop_time - start_time).split('.')[0]

    test_info = {'total_case': total_case,
                 'total_pass': total_pass,
                 'total_fail': total_fail,
                 'total_error': total_error,
                 'test_env': test_env,
                 'start_log_time': start_log_time,
                 'stop_log_time': stop_log_time,
                 'run_continue_time': run_continue_time,
                 'pass_rate': pass_rate,
                 'test_case_file': test_case_file
                 }
    return test_info
