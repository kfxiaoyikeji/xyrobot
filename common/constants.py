# -*- coding: utf-8 -*-
import os
# 高级的 文件、文件夹、压缩包 处理模块
import shutil

#获取当前app的绝对路径
APP_PATH = os.path.normpath(os.path.join(os.path.dirname(
        os.path.abspath(__file__)),os.pardir))

#存放app中使用到的所有的静态数据
DATA_PATH = os.path.join(APP_PATH, "staticData")

#默认的配置文件名
DEFULT_CONFIG_FILE_NAME = 'config.yml'
#AnyQ-QA文件名
ANYQ_QA_FILE_NAME = 'qa.csv'
#Logs path
LOGS_PATH = os.path.join(APP_PATH, "logs")

def getConfigPath():
    """
    获取默认配置文件的路径

    returns: 配置文件的存储路径
    """
    config_source = os.path.join(DATA_PATH, DEFULT_CONFIG_FILE_NAME)
    config_dst = os.path.join(APP_PATH, DEFULT_CONFIG_FILE_NAME)
    return _copyFileFromSourceToDist(config_source,config_dst)

def getAnyQPath():
    """
    获取AnyQ——QA数据集文件的路径
    returns: AnyQ——QA数据集文件的存储路径
    """
    qa_source = os.path.join(DATA_PATH, ANYQ_QA_FILE_NAME)
    qa_dst = os.path.join(APP_PATH, ANYQ_QA_FILE_NAME)
    return _copyFileFromSourceToDist(qa_source,qa_dst)

def _copyFileFromSourceToDist(fileSource,fileDist):
    if not os.path.exists(fileDist):
        shutil.copyfile(fileSource, fileDist)
    return fileDist

print(APP_PATH)
print(DEFULT_CONFIG_FILE_NAME)
print(DATA_PATH)
