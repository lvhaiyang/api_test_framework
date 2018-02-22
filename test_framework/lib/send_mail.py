# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import re
import traceback
import socket
import smtplib
import platform
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


def send_mail(logger=None, mailto_addrs=None, test_report=None, test_info=None, report_file_path1=None, report_file_path2=None):
    '''
    发送邮件模块
    :param logger:  logging 日志对象
    :param mailto_addrs:    收件人列表 ['lvhaiyang@juzifenqi.com', 'zidongceshi@juzifenqi.com']
    :param test_report:      run_casef方法返回值，列表格式测试报告
    :param report_file_path1:  excel测试报告文件路径
    :param report_file_path2:   log测试日志文件路径
    :return:    None
    '''
    logger.debug(u'开始发送邮件到 {0}'.format(mailto_addrs))
    sender = 'zidongceshi@juzifenqi.com'
    receiver = mailto_addrs
    subject = '自动化测试报告'
    smtpserver = 'smtp.qiye.163.com'
    username = 'zidongceshi@juzifenqi.com'
    password = 'JUZIfenqi3'

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
    #
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    #
    # log_path = '../report'
    # log_file = 'report_test.log'
    # log_name = os.path.join(log_path, log_file)
    #
    # # 定义日志格式
    # formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s')
    #
    # logger = logging.getLogger('qa')
    # logger.setLevel(logging.DEBUG)
    #
    # # 控制台日志设置
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter)
    #
    # # log文件设置
    # fh = logging.FileHandler(filename=log_name, mode='a', encoding='utf-8')
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(formatter)
    #
    # logger.addHandler(ch)
    # logger.addHandler(fh)

    test_report = [[u'\u6d4b\u8bd5\u7528\u4f8b\u540d\u79f0', u'\u63a5\u53e3\u540d\u79f0', u'\u63a5\u53e3\u5730\u5740', u'\u8bf7\u6c42\u5934\u90e8', u'\u8bf7\u6c42\u65b9\u5f0f', u'\u8bf7\u6c42\u6570\u636e\u683c\u5f0f', u'\u8bf7\u6c42\u53c2\u6570', u'\u6570\u636e\u5e93\u64cd\u4f5c', u'\u9884\u671f\u7ed3\u679c', '\xe5\x93\x8d\xe5\xba\x94\xe7\xbb\x93\xe6\x9e\x9c', '\xe5\x93\x8d\xe5\xba\x94\xe6\x97\xb6\xe9\x97\xb4(s)', '\xe7\x8a\xb6\xe6\x80\x81\xe7\xa0\x81', '\xe6\xb5\x8b\xe8\xaf\x95\xe7\xbb\x93\xe6\x9e\x9c', '\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u6d4b\u8bd5\u7ebf--\u5220\u9664\u8d26\u53f7\u63a5\u53e3', u'\u6d4b\u8bd5\u7ebf--\u5220\u9664\u8d26\u53f7\u63a5\u53e3', u'/rest/member/dropMember', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'get', u'x-www-form-urlencoded', u'{"mobile": "18812345678"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', 0.166, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u539f\u751f\u7528\u6237\u6ce8\u518c\u7684\u77ed\u4fe1\u9a8c\u8bc1\u7801', u'\u539f\u751f\u7528\u6237\u6ce8\u518c\u7684\u77ed\u4fe1\u9a8c\u8bc1\u7801', u'/rest/sms/sendRegisterSms', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678", "category": 0}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', 0.054, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u83b7\u53d6\u6ce8\u518c\u9a8c\u8bc1\u7801', u'\u6d4b\u8bd5\u7ebf--\u67e5\u8be2\u7528\u6237\u624b\u673a\u9a8c\u8bc1\u7801', u'/rest/sms/getSmsCode', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'get', u'x-www-form-urlencoded', u'{"mobile": "18812345678", "type": "1", "memberTag": "MemberShop"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": "027491", "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": "027491", "success": true}', 0.017, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u7528\u6237\u4e2d\u5fc3-\u6ce8\u518c', u'\u539f\u751fapp\u6ce8\u518c', u'/rest/member/memberNativeRegister', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"code": "027491", "reference": "", "mobile": "18812345678", "loginSource": "shangcheng", "source": 3, "mobileBrand": "", "mobileMaker": "", "imei": "1234", "personStatus": 0, "password": "qaz123456"}', u'Y', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "kkcVfiECNEZReNEQWTDZkg==", "token": "3df94628-71bc-4b83-9201-447fc90a4740", "registerSrc": null, "memberId": 202161107}, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "kkcVfiECNEZReNEQWTDZkg==", "token": "3df94628-71bc-4b83-9201-447fc90a4740", "registerSrc": null, "memberId": 202161107}, "success": true}', 0.097, 200, 'pass', 'pass'], [u'\u7528\u6237\u4e2d\u5fc3-\u767b\u9646', u'\u539f\u751fapp\u767b\u5f55', u'/rest/member/memberNativeLogin', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678", "loginSource": "shangcheng", "source": 3, "mobileBrand": "", "imei": "1234", "mobileMaker": "", "password": "qaz123456"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "f18812345678", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd", "registerSrc": null, "memberId": 202161107}, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "f18812345678", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd", "registerSrc": null, "memberId": 202161107}, "success": true}', 0.138, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u7528\u6237\u4e2d\u5fc3-\u83b7\u53d6\u767b\u9646\u7528\u6237\u5bf9\u8c61', u'\u539f\u751f\u53d6\u5f97\u767b\u5f55\u7528\u6237\u5bf9\u8c61', u'/rest/member/getLoginMember', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"imei": "1234", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "f18812345678", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd", "registerSrc": null, "memberId": 202161107}, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"selfReference": "f18812345678", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd", "registerSrc": null, "memberId": 202161107}, "success": true}', 0.027, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u7528\u6237\u4e2d\u5fc3-\u9000\u51fa\u767b\u9646', u'\u539f\u751fapp\u9000\u51fa\u767b\u5f55', u'/rest/member/destoryNative', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"imei": "1234", "token": "d5b7c4ef-e85f-41c4-89b2-f5c2ee4955dd"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', 0.028, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u6839\u636e\u7528\u6237\u624b\u673a\u53f7\u83b7\u53d6\u7528\u6237', u'\u6839\u636e\u7528\u6237\u624b\u673a\u53f7\u83b7\u53d6\u7528\u6237', u'/rest/member/getMemberByMobile', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "verifyFinalStatus": 0, "childId": 62161096, "email": null, "channel": null, "status": 1, "qq": null, "baseId": 202161107, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "infoMember": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "email": null, "channel": null, "status": 1, "qq": null, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "registerSrc": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "verifyFinalStatus": 0, "childId": 62161096, "email": null, "channel": null, "status": 1, "qq": null, "baseId": 202161107, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "infoMember": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "email": null, "channel": null, "status": 1, "qq": null, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "registerSrc": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "success": true}', 0.031, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u7528\u6237\u624b\u673a\u53f7\u662f\u5426\u5b58\u5728', u'\u7528\u6237\u624b\u673a\u53f7\u662f\u5426\u5b58\u5728', u'/rest/member/isMobExists', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', 0.024, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u83b7\u53d6\u7528\u6237ID\u6839\u636e\u624b\u673a\u53f7', u'\u83b7\u53d6\u7528\u6237ID\u6839\u636e\u624b\u673a\u53f7', u'/rest/member/getMemberIdByMobile', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'get', u'x-www-form-urlencoded', u'{"mobile": "18812345678"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": 202161107, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": 202161107, "success": true}', 0.032, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u8bbe\u7f6e\u652f\u4ed8\u5bc6\u7801', u'\u8bbe\u7f6e\u652f\u4ed8\u5bc6\u7801', u'/rest/member/addBalancePassword', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678", "password": "qaz123456"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "verifyFinalStatus": 0, "childId": 62161096, "email": null, "channel": null, "status": 1, "qq": null, "baseId": 202161107, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "infoMember": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "email": null, "channel": null, "status": 1, "qq": null, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "registerSrc": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "verifyFinalStatus": 0, "childId": 62161096, "email": null, "channel": null, "status": 1, "qq": null, "baseId": 202161107, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "infoMember": {"username": "xNpHQS6J6bK+/HBtsQJD5A==", "updateTime": null, "signingOrganization": null, "reference": "", "grade": 1, "idcard": null, "registerTime": 1513229554000, "zhifubao": null, "headPortrait": null, "isSmsVerify": null, "personStatus": 0, "id": 202161107, "ethnicity": null, "isProxy": 0, "idcardValidTime": null, "password": "be033b2dbe3befc7e145dbcb72cfe029", "realName": null, "source": 3, "weixin": null, "email": null, "channel": null, "status": 1, "qq": null, "weibo": null, "domiciliaryAddress": null, "integral": 0, "censusRegisterAddress": null, "verifyTime": null, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "phone": null, "birthday": null, "faceStatus": null, "idcardBackImageUrl": null, "isEmailVerify": null, "balance": 0.0, "name": "188****5678", "mobile": "18812345678", "gender": 0, "selfReference": "f18812345678", "marriage": null, "registerSrc": null, "idcardFrontImageUrl": null, "salt": "OosV09irHjwwOxtaPyc5cZ6uPfmA7gb7", "isCarrieroperator": null, "gradeValue": 0, "balancePwd": null}, "success": true}', 0.035, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c'], [u'\u901a\u7528\u53d1\u9001\u624b\u673a\u53f7', u'\u901a\u7528\u53d1\u9001\u624b\u673a\u53f7', u'/rest/sms/sendCommonSms', u'{"User-Agent": "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-DL00 Build/HUAWEINXT-DL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"}', u'post', u'x-www-form-urlencoded', u'{"mobile": "18812345678", "category": 0, "smsContent": "\u81ea\u52a8\u6d4b\u8bd5"}', u'N', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', u'{"message": "\u8bf7\u6c42\u6210\u529f", "code": "S_SUC:000000", "pager": null, "result": true, "success": true}', 0.036, 200, 'pass', '\xe6\x9c\xaa\xe5\xbc\x80\xe5\x90\xaf\xe6\x95\xb0\xe6\x8d\xae\xe5\xba\x93\xe6\xa0\xa1\xe9\xaa\x8c']]

    # report_file_path1 = '../report/report2017_12_14_11_02_08.xls'
    # report_file_path2 = '../report/report2017_12_14_11_02_08.log'
    # mailto_addrs = ['zidongceshi@juzifenqi.com']
    # send_mail(logger=logger, mailto_addrs=mailto_addrs, test_report=test_report, report_file_path1=report_file_path1, report_file_path2=report_file_path2)

    body = generate_mail_body(test_report=test_report)
    # print body