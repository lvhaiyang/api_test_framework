# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from runcase.models import Upload
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
        if i == 'upload':
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
        # if cf.is_valid():
        try:
            filename = cf.cleaned_data['filename']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 101, 'msg': '测试用例信息获取失败'})
        try:
            emailaddr = cf.cleaned_data['email']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 102, 'msg': 'email信息获取失败'})
        try:
            test_env = cf.cleaned_data['env']
        except Exception as e:
            print(e.args)
            return JsonResponse({"code": 103, 'msg': '测试环境信息获取失败'})

        #写入数据库
        f = Upload()
        f.file_path = filename
        f.save()

        # 上传的测试用例移动到对应位置
        src_testcase_file = os.path.join('test_framework', 'upload', str(filename))
        dst_testcase_file = os.path.join('test_framework', flag, str(filename))
        shutil.move(src_testcase_file, dst_testcase_file)

        # 修改配置文件
        for i in os.listdir(os.path.join('test_framework', flag)):
            if re.search(test_env, i):
                shutil.copyfile(os.path.join('test_framework', flag, i), os.path.join('test_framework', flag, 'config.py'))

        sys.path.append(os.path.join('test_framework', flag))
        import run_test
        env_path = run_test.__file__
        env_path = env_path.split('run_test.py')[0]
        print(env_path)
        excel_file_path = dst_testcase_file
        mail_addrs = emailaddr.split(',')
        run_test.main(excel_file_path=excel_file_path, mail_switch=1, mail_addrs=mail_addrs, env_path=env_path)

        return JsonResponse({"code": 0, 'msg': '请求成功, 测试用例：{0} 执行完成；邮件通知：{1}'.format(filename, emailaddr)})

    else:
        return HttpResponse("<h1>hello api test framework</h1>", content_type="text/html")


