#!encoding=utf-8

from __future__ import unicode_literals
import logging
import os


def capture_log(run_time, env_path):
    '''
    创建日志
    :param run_time:  datatime
    :return:   日志对象
    '''
    log_path = os.path.join(env_path, 'test_report')
    log_file = 'report{}.log'.format(run_time)
    log_name = os.path.join(log_path, log_file)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s')

    logger = logging.getLogger('qa')
    logger.setLevel(logging.DEBUG)

    # 控制台日志设置
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # log文件设置
    fh = logging.FileHandler(filename=log_name, mode='a', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    for i in logger.handlers:
        logger.handlers.remove(i)

    logger.handlers.append(ch)
    logger.handlers.append(fh)

    return logger





