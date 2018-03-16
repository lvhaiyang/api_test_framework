# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import re
import traceback
import socket
import smtplib
import platform
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def generate_mail_body(test_report=None, test_info=None):
    '''
    生成邮件内容
    :param test_report:     run_case方法返回值，列表格式测试报告
    :return:        html 格式测试报告
    '''
    html_report = u'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html><body>'

    html_style = u'''
    <style>
    table{table-layout: fixed;word-break: break-all; word-wrap: break-word;}
    award-name{-o-text-overflow:ellipsis;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;width:100%;}
    </style>
    '''
    html_report = html_report + html_style

    html_test_summary = u'''<h1>自动化测试报告</h1>  
    <font style="font-weight:bold; size="4">测试环境：</font> <font>&nbsp;&nbsp; %(test_env)s</font><br>
    <font style="font-weight:bold; size="4">测试用例：</font> <font>&nbsp;&nbsp; %(test_case_file)s</font><br>
    <font style="font-weight:bold; size="4">开始时间：</font> <font>&nbsp;&nbsp; %(start_log_time)s</font><br>
    <font style="font-weight:bold; size="4">结束时间：</font> <font>&nbsp;&nbsp; %(stop_log_time)s</font><br>
    <font style="font-weight:bold; size="4">测试用时：</font> <font>&nbsp;&nbsp; %(run_continue_time)s</font><br>    
    <font style="font-weight:bold; size="4">测试概要：</font> <font>&nbsp;&nbsp; pass: %(total_pass)s &nbsp;   fail: %(total_fail)s  &nbsp;  error:  %(total_error)s</font><br>
    <font style="font-weight:bold; size="4">通&nbsp;过&nbsp;率：</font> <font>&nbsp;&nbsp; %(pass_rate)s</font><br><br>
    ''' % test_info

    html_report = html_report + html_test_summary

    html_report = html_report + u'<b>详细测试报告请查看附件excel文件, 运行日志请查看附件log文件</b>'
    html_report = html_report + u'<table border="1" cellspacing="0">'
    for index_test_report, report in enumerate(test_report):
        if report[-2] == 'pass':
            html_report = html_report + u'<tr bgcolor=#ADFF2F>'
        elif report[-2] == 'fail':
            html_report = html_report + u'<tr bgcolor=#B22222>'
        elif report[-2] == 'error':
            html_report = html_report + u'<tr bgcolor=#9400D3>'

        for index, i in enumerate(report):
            # print type(i), i
            if index < 3:
                html_report = html_report + u'<td style="white-space:nowrap;">'
                html_report = html_report + i
                html_report = html_report + u'</td>'
            elif index > 9:
                html_report = html_report + u'<td style="white-space:nowrap;">'
                html_report = html_report + i
                html_report = html_report + u'</td>'

        html_report = html_report + u'</tr>'
    html_report = html_report + u'</table></body></html>'

    return html_report


def send_mail(mailto_addrs=None, test_report=None, test_info=None, report_file_path1=None, report_file_path2=None):
    '''
    发送邮件模块
    :param logger:  logging 日志对象
    :param mailto_addrs:    收件人列表 ['x@xx.com', 'x@x.com']
    :param test_report:      run_casef方法返回值，列表格式测试报告
    :param report_file_path1:  excel测试报告文件路径
    :param report_file_path2:   log测试日志文件路径
    :return:    None
    '''
    logger = logging.getLogger('qa')
    logger.debug(u'开始发送邮件到 {0}'.format(mailto_addrs))
    sender = 'xxx@xxx.com'
    receiver = mailto_addrs
    subject = '自动化测试报告'
    smtpserver = 'smtp.xx.com'
    username = 'xx@xxx.com'
    password = 'xxx'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['to'] = ','.join(receiver)

    body = generate_mail_body(test_report=test_report, test_info=test_info)

    mail_body = MIMEText(body, 'html', 'utf-8')
    msg.attach(mail_body)

    part = MIMEApplication(open(report_file_path1, 'rb').read())
    if re.match('Win', platform.system()):
        part.add_header('Content-Disposition', 'attachment', filename=report_file_path1.split('\\')[-1])
    else:
        part.add_header('Content-Disposition', 'attachment', filename=report_file_path1.split('/')[-1])
    msg.attach(part)

    part = MIMEApplication(open(report_file_path2, 'rb').read())
    if re.match('Win', platform.system()):
        part.add_header('Content-Disposition', 'attachment', filename=report_file_path2.split('\\')[-1])
    else:
        part.add_header('Content-Disposition', 'attachment', filename=report_file_path2.split('/')[-1])
    msg.attach(part)

    try:
        socket.setdefaulttimeout(60)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        logger.debug(u'邮件发送：成功')
    except:
        logger.debug(u'邮件发送：失败')


if __name__ == '__main__':

    import os
    import logging
