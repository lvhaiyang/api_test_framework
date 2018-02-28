#!encoding=utf-8

from __future__ import unicode_literals
import os
import requests
import traceback
from lib.core import *
from config import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ApiTemplate(object):
    '''
    这个类定义了 api 模板
    '''

    def __init__(self, base_url=None, session=None, request_type=None, send_data_type=None, send_data=None, headers=None, expect_data=None, json_file_path=None, api_url_suffix=None, logger=None):
        '''
        这个方法初始化接口测试所需的所有数据
        :param base_url:        接口请求的域名
        :param session:         resquests库中session对象
        :param request_type:    接口请求方式
        :param send_data_type:  接口请求数据格式
        :param send_data:       接口请求数据
        :param headers:         接口请求headers
        :param expect_data:     测试用例预期结果
        :param json_file_path:  保存返回值临时json文件路径
        :param api_url_suffix:  接口地址后缀名
        :param logger:          logging模块 logging对象
        '''
        self.base_url = base_url
        self.session = session
        self.request_type = request_type
        self.send_data_type = send_data_type
        self.send_data = send_data
        self.headers = headers
        self.expect_data = expect_data
        self.json_file_path = json_file_path
        self.api_url = None     #api路径
        self.response = None    #requests 接口请求的对象
        self.response_time = None       #接口响应时间
        self.response_json_data = {}    #接口响应json数据
        self.save_json_data = load_json_file(self.json_file_path)       #所有请求接口的返回值组成的字典，键为接口的名字，值为接口返回json值
        self.api_url_suffix = api_url_suffix        #接口地址后缀如：.json .html  .so 没有后缀为空
        self.logger = logger
        self.save_key = None        #接口名字

    def get_api_info(self):
        '''
        这个方法用于获取接口信息，api_url, save_key
        :return:
        '''
        self.save_key = os.path.basename(__file__).split('.')[0]
        self.api_url = '/{}'.format(self.save_key.replace('_', '/'))
        if self.api_url_suffix is not None:
            self.api_url = '{0}.{1}'.format(self.api_url, self.api_url_suffix)

        # print api_url

    def run(self):
        '''
        执行接口测试方法
        :return:
        '''
        self.get_api_info()
        self.change_headers()
        self.change_send_data()

        self.logger.debug(u'请求参数格式：{}'.format(self.send_data_type))
        self.logger.debug(u'请求参数：{}'.format(self.send_data))
        url = '{0}{1}'.format(self.base_url, self.api_url)
        self.logger.debug(u'请求地址：{}'.format(url))
        self.logger.debug(u'请求方式：{}'.format(self.request_type))
        self.response = request_mode(session=self.session, request_type=self.request_type, url=url, data_type=self.send_data_type, data=self.send_data, headers=self.headers, logger=self.logger)
        try:
            self.response_time = int(self.response.elapsed.microseconds)/1000
            self.response_time = int(self.response_time)/1000.0
            self.logger.debug(u'接口响应时间  {0}秒'.format(self.response_time))
        except:
            self.logger.debug(u'接口响应时间获取失败')

        try:
            self.response_json_data = self.response.json()
        except:
            self.logger.debug(u'没有发现json返回值')

        self.save_response_data()
        self.change_expect_data()
        self.save_request_data()

        # if check_py_version() == '2.x':
        #     self.logger.debug(u'预期结果：{}'.format(json.dumps(self.expect_data, ensure_ascii=False, encoding='UTF-8')))
        # elif check_py_version() == '3.x':
        #     self.logger.debug(u'预期结果：{}'.format(json.dumps(self.expect_data, ensure_ascii=False)))
        save_json_file(self.json_file_path, self.save_json_data)

        res, status_code, result = verify_mode(self.response, expect_data=self.expect_data, logger=self.logger)
        return res, status_code, result, self.response_time

    def change_headers(self):
        '''
        更新headers（用户修改excel测试用例中headers列的值）
        使用时需要对方法重写
        :return:
        '''
        headers = self.headers
        params_data = self.save_json_data
        '''
        headers['authorization'] = params_data['authorization']
        '''

    def change_send_data(self):
        '''
        更新send_data（用户修改excel测试用例中send_data列的值）
        使用时需要对方法重写
        :return:
        '''
        data = self.send_data
        params_data = self.save_json_data
        '''
        data['authorization'] = params_data['authorization']
        '''

    def change_expect_data(self):
        '''
        更新expect_data（用户修改excel测试用例中expect_data列的值）
        使用时需要对方法重写
        :return:
        '''
        data = self.expect_data
        params_data = self.save_json_data
        '''
        data['authorization'] = params_data['authorization']
        '''

    def save_response_data(self):
        '''
        保存接口响应数据
        :return:
        '''
        response_json_data = self.response_json_data
        data = self.save_json_data
        save_key = self.save_key
        data[save_key] = {}

        try:
            data[save_key] = response_json_data
            self.logger.debug(u'保存响应数据成功，保存位置 data["{0}"]'.format(save_key))
        except:
            self.logger.debug(traceback.format_exc())
            self.logger.debug(u'保存响应数据失败')

    def replace_data(self):
        '''
        替换 self.headers, self.send_data, self.expect_data
        :return:
        '''
        return self.headers, self.send_data, self.expect_data

    def change_data(self, name, data, replace_data, cmds):
        '''
        替换excel 读取的测试用例内容
        :param name:  数据名称
        :param data:  数据内容 字典格式
        :param replace_data:  替换内容
        :param cmds:  替换命令
        :return:
        '''
        replace_path_list = self.generator_replace_path(data)
        self.logger.debug(u'开始替换 {0}'.format(name))
        self.logger.debug(u'原始的{0}信息为：{1}'.format(name, data))

        for p in replace_path_list:
            for cmd in cmds:
                if p == cmd.split('=')[0].split(' ')[0]:
                    try:
                        self.logger.debug(u'执行替换命令 {0}'.format(cmd))
                        exec(cmd)
                    except:
                        self.logger.debug(traceback.format_exc())
                        self.logger.debug(u'替换命令 {0} 执行失败 ！！！！！！！！！！'.format(cmd))
                        self.logger.debug(u'执行替换命令 需要前置条件接口 {} 执行完成'.format(cmd.split('replace_data[')[1].split(']')[0]))

        self.logger.debug(u'替换后{0}信息为：{1}'.format(name, data))

    def save_request_data(self):
        '''
        保存接口响应数据
        :return:
        '''
        request_json_data = self.send_data
        data = self.save_json_data
        save_key = self.save_key
        if 'send_data' not in data.keys():
            data['send_data'] = {}

        try:
            data['send_data'][save_key] = request_json_data
            self.logger.debug(u'保存请求数据成功，保存位置 data["send_data"]["{0}"]'.format(save_key))
        except:
            self.logger.debug(traceback.format_exc())
            self.logger.debug(u'保存请求数据失败')

    def find_replace_data(self, replace_lists, data, father_key=''):
        for key in data.keys():
            if isinstance(data[key], dict):
                new_data = data[key]
                if father_key == '':
                    self.find_replace_data(replace_lists, new_data, father_key='{0}'.format(key))
                else:
                    self.find_replace_data(replace_lists, new_data, father_key='{0}.{1}'.format(father_key, key))
            else:
                if data[key] == '%replace%':
                    if father_key == '':
                        replace_lists.append('{0}'.format(key))
                    else:
                        replace_lists.append('{0}.{1}'.format(father_key, key))

    def generator_replace_path(self, data):
        replace_lists = []
        self.find_replace_data(replace_lists, data)
        path_list = []
        for i in replace_lists:
            path = 'data'
            for j in i.split('.'):
                path = path + "['{0}']".format(j)
            path_list.append(path)
        return path_list




