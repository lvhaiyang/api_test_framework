#encoding=utf-8

from __future__ import unicode_literals
import traceback
import logging
from lib.core import *


if check_py_version() == '2.x':
    import MySQLdb as mysql
elif check_py_version() == '3.x':
    import pymysql as mysql


class MysqlConnection(object):
    '''
    这个类定义了一个连接MQSQL，增删改查的模板
    '''
    def __init__(self, host, port, user, password, db_name, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.charset = charset
        self.logger = logging.getLogger('qa')

    def insert(self, sql):
        try:
            self.logger.debug(u'开始执行 insert 语句  {0}'.format(sql))

            db = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                     db=self.db_name, charset=self.charset)

            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            db.close()
            self.logger.debug(u'insert 语句  {0} 执行成功 '.format(sql))
        except:
            self.logger.debug(u'insert 语句  {0} 执行失败 '.format(sql))
            self.logger.debug(traceback.format_exc())
            return 'db_insert_error'

    def delete(self, sql):
        try:
            self.logger.debug(u'开始执行 delete 语句  sql : {0}'.format(sql))
            db = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                      db=self.db_name, charset=self.charset)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            db.close()
            self.logger.debug(u'delete 语句  {0} 执行成功 '.format(sql))
        except:
            self.logger.debug(u'delete 语句  {0} 执行失败 '.format(sql))
            return 'db_delete_error'

    def update(self, sql):
        try:
            self.logger.debug(u'开始执行 update 语句  sql : {0}'.format(sql))
            db = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                      db=self.db_name, charset=self.charset)
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            db.close()
            self.logger.debug(u'update 语句  {0} 执行成功 '.format(sql))
        except:
            self.logger.debug(u'update 语句  {0} 执行失败 '.format(sql))
            return 'db_update_error'

    def select(self, sql):
        try:
            self.logger.debug(u'开始执行 select 语句  sql : {0}'.format(sql))
            db = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                      db=self.db_name, charset=self.charset)
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            if results == ():
                self.logger.debug(u'select 语句 查询结果为空')
                return 'db_select_pass', ''
            else:
                self.logger.debug(u'select 语句 查询结果为 {0}'.format(results[0][0]))
                return 'db_select_pass', results[0][0]
        except:
            self.logger.debug(u'select 语句  执行失败')
            return 'db_select_error', ''


class DatabaseCheckTemplate(object):
    '''
    这个类使用需要重写，定义测试用例数据库初始化和验证的模板
    1、先清理数据库环境 如果有上次的测试数据, 把上次测试的数据删除
    2、数据库中插入需要的数据
    3、检查运行接口测试之后数据库存储, 更新, 删除的数据情况
    '''

    MYSQL = None
    # config文件中配置的数据库名称
    # name = 'ShangChengConfig'
    name = ''

    def __init__(self, config_mode, send_data=None, json_file_path=None):
        self.send_data = send_data
        self.logger = logging.getLogger('qa')
        self.save_json_data = load_json_file(json_file_path)  # 所有请求接口的返回值组成的字典，键为接口的名字，值为接口返回json值
        self.logger.debug(u'读取数据库配置为  {0}'.format(self.name))
        try:
            self.host = eval('config_mode.{0}.HOST'.format(self.name))
            self.port = eval('config_mode.{0}.PORT'.format(self.name))
            self.user = eval('config_mode.{0}.USER'.format(self.name))
            self.password = eval('config_mode.{0}.PASSWORD'.format(self.name))
            self.db_name = eval('config_mode.{0}.DB'.format(self.name))
            self.charset = eval('config_mode.{0}.CHARSET'.format(self.name))
            self.logger.debug(u'数据库 HOST    {0}'.format(self.host))
            self.logger.debug(u'数据库 PORT    {0}'.format(self.port))
            self.logger.debug(u'数据库 USER    {0}'.format(self.user))
            self.logger.debug(u'数据库 PASSWD  {0}'.format(self.password))
            self.logger.debug(u'数据库 DB      {0}'.format(self.db_name))
            self.logger.debug(u'数据库 CHARSET      {0}'.format(self.charset))

            self.MYSQL = MysqlConnection(host=self.host, port=self.port, user=self.user, password=self.password,
                                         db_name=self.db_name, charset=self.charset)
        except:
            self.logger.debug(traceback.format_exc())
            self.logger.debug(u'连接数据库失败')

    def set_up(self):
        '''
        初始化数据库
        :return:
        '''
        MYSQL = self.MYSQL
        # 清理数据库
        # eg. 'DELETE FROM turn_log WHERE prize_name = '谢谢参与2';'
        sql = "DELETE FROM turn_log WHERE prize_name = '谢谢参与2'"
        result1 = MYSQL.delete(sql=sql)
        # print result1

        # 插入测试数据
        # eg. 'INSERT INTO `juzi`.`turn_log` (`user_id`, `prize_name`, `prize_id`, `add_time`, `recharge`, `phone`, `re_time`, `money`, `sharenum`) VALUES ('521206', '谢谢参与2', '5', '2017-11-16 10:43:38', '0', NULL, NULL, NULL, '0');'
        sql = "INSERT INTO `juzi`.`turn_log` (`user_id`, `prize_name`, `prize_id`, `add_time`, `recharge`, `phone`, `re_time`, `money`, `sharenum`) VALUES ('521206', '谢谢参与2', '5', '2017-11-16 10:43:38', '0', NULL, NULL, NULL, '0')"
        result2 = MYSQL.insert(sql=sql)
        # print result2

    def verify_mode(self):
        '''
        验证数据库
        :return:
        '''
        MYSQL = self.MYSQL
        # 查询到一个数据的sql
        # eg. 'SELECT prize_name FROM turn_log where user_id = '521206''
        sql = "SELECT prize_name FROM turn_log where prize_name = '谢谢参与2'"
        value = MYSQL.select(sql=sql)
        expect_string = ''
        result = self.expect_mode(value, expect_string)

        if result == 'pass':
            return 'pass'
        else:
            return 'fail'

    def expect_mode(self, values, expect_strings):
        '''
        对比数据库查询结果
        :param value:   数据库查询结果（结果必须为一个字符串）
        :param expect_string:  预期结果
        :return:
        '''
        self.logger.debug(u'开始数据库校验')
        results = []
        if not values:
            return 'pass'
        for i, value in enumerate(values):
            result = ''
            expect_string = expect_strings[i]
            value = '{}'.format(value)
            expect_string = '{}'.format(expect_string)
            if check_py_version() == '2.x':
                expect_string = expect_string
            elif check_py_version() == '3.x':
                expect_string = expect_string

            if value == expect_string:
                self.logger.debug(u'数据库校验：通过')
                self.logger.debug(u'预期结果：{}'.format(expect_string))
                self.logger.debug(u'实际结果：{}'.format(value))
                result = 'pass'
            else:
                self.logger.debug(u'数据库校验：失败')
                self.logger.debug(u'预期结果：{}'.format(expect_string))
                self.logger.debug(u'实际结果：{}'.format(value))
                result = 'fail'

            results.append(result)

        if 'fail' in results:
            return 'fail'
        else:
            return 'pass'

    def check_db_connect(self):
        '''
        检查数据库连接状态
        :return:  数据库连接状态
        '''
        self.logger.debug(u'开始检查数据库配置')
        if self.MYSQL is None:
            self.logger.debug(u'数据库配置检查： 失败')
            return 'db_connect_error'
        else:
            self.logger.debug(u'数据库配置检查： 成功')
            return 'db_connect_success'

    def run_set_up(self):
        '''
        执行初始化数据库
        :return:
        '''
        self.logger.debug(u'开始初始化数据库')
        if self.check_db_connect() == 'db_connect_success':
            return self.set_up()
        else:
            if self.name == '':
                return 'error'
            else:
                return 'error'

    def run_verify(self):
        '''
        执行数据库校验
        :return:
        '''
        self.logger.debug(u'开始进行数据库校验')
        if self.check_db_connect() == 'db_connect_success':
            return self.verify_mode()
        else:
            if self.name == '':
                return 'error'
            else:
                return 'error'

    def execute_sqls(self, insert_sqls=None, delete_sqls=None, update_sqls=None, select_sqls=None):

        # insert
        if insert_sqls != [] and insert_sqls is not None:
            for insert_sql in insert_sqls:
                self.MYSQL.insert(insert_sql)

        # delete_sqls
        if delete_sqls != [] and delete_sqls is not None:
            for sql in delete_sqls:
                self.MYSQL.delete(sql)

        # update_sqls
        if update_sqls != [] and update_sqls is not None:
            for sql in update_sqls:
                self.MYSQL.update(sql)

        # select_sqls
        if select_sqls != [] and select_sqls is not None:
            result = []
            for sql in select_sqls:
                result.append(self.MYSQL.select(sql)[1])
            return result
        else:
            return []


if __name__ == '__main__':
    from config import *
    name = 'ShangChengConfig'
    host = eval(name).HOST
    port = eval(name).PORT
    user = eval(name).USER
    password = eval(name).PASSWORD
    db_name = eval(name).DB


    db = mysql.connect(host=host, port=port, user=user, passwd=password, db=db_name)
    # sql = 'insert into login_user (username, password) values (%s, %s)'
    # param = (('hylv', '123456'),)
    # con.insert(sql, param)

    # sql = 'update login_user set username=%s, password=%s where id=10'
    # param = ('lvhaiyang', '123456')
    # con.update(sql, param)

    sql = "SELECT prize_name FROM turn_log where prize_name = '谢谢参与3'"
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    # print results

    # sql = 'delete from login_user where id=1'
    # con.delete(sql)


    db.close()
