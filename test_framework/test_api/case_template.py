#!encoding=utf-8

from __future__ import unicode_literals
import traceback
from lib.api_template import *
from lib.mysql import *
from config import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CASE_INFO = ''


# 接口部分
class ApiTest(ApiTemplate):

    def get_api_info(self):
        self.save_key = os.path.basename(__file__).split('.')[0]
        self.api_url = '/{}'.format(self.save_key.replace('_', '/'))
        if self.api_url_suffix is not None:
            self.api_url = '{0}.{1}'.format(self.api_url, self.api_url_suffix)

    def change_headers(self):
        headers = self.headers
        params_data = self.save_json_data
# 》》》》》》》》
        #  step 1 第一个需要修改的地方
        # 如果需要修改 headers 中的信息 按照下面的格式修改
        # cmds = ["data['authorization'] = replace_data['login']['token']",
        #         "data['authorization'] = replace_data['login']['token']"]
        cmds = []

        self.change_data(u'headers', headers, params_data, cmds)

    def change_send_data(self):
        data = self.send_data
        params_data = self.save_json_data
# 》》》》》》》》
        #  step 2 第二个需要修改的地方
        # 如果需要修改 data 中的信息 按照下面的格式修改
        # cmds = ["data['data'] = replace_data['termi_mallHome_getAreaList']['data']",
        #         "data['data'] = replace_data['termi_mallHome_getAreaList']['data']"]
        cmds = []

        self.change_data(u'send_data', data, params_data, cmds)

    def change_expect_data(self):
        data = self.expect_data
        params_data = self.save_json_data
# 》》》》》》》》
        #  step 3 第三个需要修改的地方
        # 如果需要修改 expect_data 中的信息 按照下面的格式修改
        # cmds = ["data['data'] = replace_data['termi_mallHome_getAreaList']['data']",
        #         "data['data'] = replace_data['termi_mallHome_getAreaList']['data']"]
        cmds = []

        self.change_data(u'expect_data', data, params_data, cmds)


# 数据库部分
class DatabaseCheck(DatabaseCheckTemplate):
    '''
    先清理数据库环境 如果有上次的测试数据, 把上次测试的数据删除
    数据库中插入需要的数据
    检查运行接口测试之后数据库存储, 更新, 删除的数据情况
    '''
    MYSQL = None

# 》》》》》》》》
    #  step 1 第一个需要修改的地方
    # config文件中配置的数据库名称
    # name = 'ShangChengConfig'
    name = ''



