# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from runcase.models import Upload
from importlib import import_module
import os
import sys
import datetime
import random
import shutil
import platform
import re


# Create your views here.
class CaseForm(forms.Form):
    filename = forms.FileField()
    email = forms.CharField()
    env = forms.CharField()


@csrf_exempt
def test_api(request):
    # 按照时间创建临时执行测试用例目录
    format_time = "%Y%m%d%H%M%S"
    post_time = datetime.datetime.now()
    for i in os.listdir('test_framework'):
        if i in ['__init__.py', '__pycache__', 'upload']:
            continue
        try:
            old_post_time = datetime.datetime.strptime(i[:14], format_time)
            if (post_time - old_post_time).days > 5:
                # shutil.rmtree(os.path.join('test_framework', i))
                if re.match('Win', platform.system()):
                    os.system("rd/s/q  test_framework\{0}".format(i))
                else:
                    os.system("rm -rf  test_framework/{0}".format(i))
        except Exception as e:
            print('删除时间设置错误')
            print(i)
            print(e)

    r = str(random.random()).split('.')[1]
    flag = post_time.strftime(format_time) + r

    # 测试框架复制到对应目录下
    src_framework = os.path.join('..', 'test_framework')
    dst_framework = os.path.join('test_framework', flag)
    shutil.copytree(src_framework, dst_framework)

    # 上传测试用例post请求
    if request.method == "POST":
        cf = CaseForm(request.POST, request.FILES)
        print(cf)
        try:
            filename = cf.cleaned_data['filename']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 101, 'msg': 'filename不能为空'})
        try:
            emailaddr = cf.cleaned_data['email']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 102, 'msg': 'email不能为空'})
        try:
            test_env = cf.cleaned_data['env']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 103, 'msg': 'test_env不能为空'})

        #写入数据库
        f = Upload()
        f.run_dir = flag
        f.file_path = filename
        f.save()

        results = Upload.objects.all().values_list('run_dir', 'file_path')  # 取出run_dir和file_path列，并生成一个列表
        print(results)
        filename = ''
        for result in results:
            if result[0] == flag:
                filename = result[1].split('/upload/')[1]

        # 上传的测试用例移动到对应位置
        src_testcase_file = os.path.join('test_framework', 'upload', str(filename))
        dst_testcase_file = os.path.join('test_framework', flag, str(filename))
        shutil.move(src_testcase_file, dst_testcase_file)

        # 清空数据库
        Upload.objects.filter(run_dir=flag).delete()

        # 修改配置文件
        for i in os.listdir(os.path.join('test_framework', flag)):
            if re.match('config', i):
                if re.search(test_env, i):
                    shutil.copyfile(os.path.join('test_framework', flag, i), os.path.join('test_framework', flag, 'config.py'))

        sys.path.append('test_framework')
        sys.path.append(os.path.join('test_framework', flag))
        mode_name = 'test_framework.{}.run_test'.format(flag)
        run_test = import_module(mode_name)
        # print(sys.path)
        env_path = run_test.__file__
        env_path = env_path.split('run_test.py')[0]
        print(u'测试用例执行路径: ', env_path)
        excel_file_path = dst_testcase_file
        mail_addrs = emailaddr.split(',')
        result = run_test.main(excel_file_path=excel_file_path, mail_switch=1, mail_addrs=mail_addrs, env_path=env_path)

        sys.path.remove(os.path.join('test_framework', flag))
        sys.path.remove('test_framework')

        if result == '测试用例读取失败':
            return JsonResponse({"code": 104, 'msg': '测试用例读取失败, 请检查excel测试用例文件'})

        return JsonResponse({"code": 0, 'msg': '请求成功', 'data': {'测试环境': test_env, '测试用例': '{0}'.format(filename), '邮件通知': emailaddr}})

    else:
        return HttpResponse("<h1>hello api test framework</h1>", content_type="text/html")


