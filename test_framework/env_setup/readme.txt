环境安装：
python2 环境
1、下载python3.6安装包，默认安装   地址： https://www.python.org/downloads/
2、cmd窗口执行命令 pip install requests --upgrade
3、cmd窗口执行命令 pip install MySQLdb
4、cmd窗口进入到env_setup目录执行命令 easy_install xlrd-1.0.0
5、cmd窗口进入到env_setup目录执行命令 easy_install xlwt-1.3.0
6、cmd窗口进入到env_setup目录执行命令 easy install xlutils-2.0.0


python3 环境
1、下载python3.6安装包，默认安装   地址： https://www.python.org/downloads/
2、cmd窗口执行命令 pip install requests --upgrade
3、cmd窗口执行命令 pip install PyMySQL
4、cmd窗口进入到env_setup目录执行命令 easy_install xlrd-1.0.0
5、cmd窗口进入到env_setup目录执行命令 easy_install xlwt-1.3.0
6、cmd窗口进入到env_setup目录执行命令 easy install xlutils-2.0.0


使用方法：
1、执行测试用例
    在juzitest_framework目录下执行命令： python run_test.py  -t 测试用例xls文件名

2、编写测试用例
    测试用例为 .xls 文件，存放目录 test_data 格式参考已有测试用例

3、查看报告
    报告为 .xls文件， 存放目录 report
