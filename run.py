# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/14 16:33
@Author     : 测试工程师Jane
@FileName   : run.py
@Description:
'''

import click
import pytest
import os
from tools.createcasefile import CreateCaseFile
import sys
from tools import getyapi


#
# @click.command()
# @click.option('--init', type=str, help="初始化一个接口测试项目")
# @click.option('--cache', type=str, help="自动创建测试用例可执行文件")
# @click.option('--run', type=str, help="执行指定目录的测试用例")
# @click.option('--s', type=str, default='./setting.yaml', help="指定配置文件")
# def run(**options):
#     print(options)
#     if options['cache']:
#         create_yaml_file(options['cache'])

if __name__ == '__main__':
    CreateCaseFile().create_temp_case_file()
    pytest.main(['-s', '-q', '--alluredir', './result/'])
    os.system("allure generate ./result/ -o ./allure-report/ --clean")
    os.system("allure open -h 127.0.0.1 -p 8883 ./allure-report/")



# import click
# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)
# if __name__ == '__main__':
#     hello()