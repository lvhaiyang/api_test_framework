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

    def set_up(self):
        '''
        初始化数据库
        :return:
        '''
        MYSQL = self.MYSQL
        # 》》》》》》》》
        #  step 2 第二个需要修改的地方
        # 清理数据库
        # delete_sqls = ["DELETE FROM m_index_like_details WHERE scene_id = '999'",
        #                "DELETE FROM m_index_like_details WHERE scene_id = '888'"]

        delete_sqls = []
        self.execute_sqls(delete_sqls=delete_sqls)

        # 》》》》》》》》
        #  step 3 第三个需要修改的地方
        # 插入测试数据
        # insert_sqls = ["INSERT INTO `m_index_like_details` (`scene_id`, `scene_title`, `like_user`, `like_time`, `update_time`, `like_state`, `user_device_num`, `spare_field3`) VALUES ('888', NULL, '62160899', '2017-12-28 11:37:04', NULL, '1', NULL, NULL)",
        #                "INSERT INTO `m_index_like_details` (`scene_id`, `scene_title`, `like_user`, `like_time`, `update_time`, `like_state`, `user_device_num`, `spare_field3`) VALUES ('999', NULL, '62160899', '2017-12-28 11:37:04', NULL, '1', NULL, NULL)"]

        insert_sqls = []

        self.execute_sqls(insert_sqls=insert_sqls)

    def verify_mode(self):
        MYSQL = self.MYSQL

        # 》》》》》》》》
        #  step 4 第四个需要修改的地方（查询sql语句， 需要验证的字段）
        # 查询到一个数据的sql
        # 需要验证的字段
        # select_sqls = ["SELECT scene_id FROM m_index_like_details where scene_id = '999'",
        #                "SELECT scene_id FROM m_index_like_details where scene_id = '999'"]
        # expect_strings = ['999', '999']

        select_sqls = []
        expect_strings = []

        values = self.execute_sqls(select_sqls=select_sqls)
        result = self.expect_mode(values, expect_strings)
        return result


