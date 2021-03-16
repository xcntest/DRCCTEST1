# -*- coding:utf-8 -*-
'''
@Time       : 2021/2/15 16:32
@Author     : 测试工程师Jane
@FileName   : logs.py
@Description: 封装日志输出方法
'''

import logging
import os
import time

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'

def create_file(filename):
    """
     创建日志文件
    :param filename: 日志文件路径
    :return:
    """
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass

def set_handler(levels):
    #输出日志到控制台
    logger.addHandler(MyLog.stream_handler)
    #输出日志文件到文件
    if levels == 'debug':
        logger.addHandler(MyLog.debug_handler)
    elif levels == 'error':
        logger.addHandler(MyLog.err_handler)
    else:
        logger.addHandler(MyLog.handler)


def remove_handler(levels):
    if levels == 'debug':
        logger.removeHandler(MyLog.debug_handler)
    elif levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)

def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))

class MyLog:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path+'/Log/info.log'
    err_file = path+'/Log/err.log'
    debug_file = path+'/Log/debug.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'
    #日志输入出handler设置
    handler = logging.FileHandler(log_file,mode="w", encoding='utf-8')
    err_handler = logging.FileHandler(err_file,mode="w", encoding='utf-8')
    debug_handler = logging.FileHandler(debug_file,mode="w", encoding='utf-8')
    stream_handler = logging.StreamHandler()


    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')


if __name__ == "__main__":
    log = MyLog()
    log.debug("This is debug message")
    log.info("This is info message")
    log.warning("This is warning message")
    log.error("This is error")
    log.critical("This is critical message")
