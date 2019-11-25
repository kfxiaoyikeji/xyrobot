# -*- coding: utf-8 -*-
# sudo apt-get install python-yaml
import yaml
import os
from . import constants

#定义一个_config字典
_config = {}
has_init = False

def reload():
    """
    重新加载配置
    """
    print('配置文件发生变更，重新加载配置文件')
    init()
    
def init():
    global has_init
    configFile = constants.getConfigPath()
    print(constants.getConfigPath())
    if not os.path.exists(constants.getConfigPath()) :
        configFile = constants.getConfigPath()
        print('Sorry,Your Config file is not exist.Now,copying config file to {}'.format(configFile))
    has_init = True
    global _config
    # Read config
    print("Trying to read config file: '%s'", configFile)
    try:
        with open(configFile,"r") as f:
            _config = yaml.safe_load(f)
    except Exception as e:
        print('Reading Config file {} failed,{}'.format(configFile,e)) 
        raise
        
def get_path(items, default=None):
    global _config
    curConfig = _config
    if isinstance(items, str) and items[0] == '/':
        items = items.split('/')[1:]
    for key in items:
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            print("/%s not specified in profile, defaulting to "
                            "'%s'", '/'.join(items), default)
            return default
    return curConfig


def has_path(items):
    global _config
    curConfig = _config
    if isinstance(items, str) and items[0] == '/':
        items = items.split('/')[1:]
    else:
        items = [items]
    for key in items:
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            return False
    return True


def has(item):
    """
    判断配置里是否包含某个配置项

    :param item: 配置项名
    :returns: True: 包含; False: 不包含
    """
    return has_path(item)


def get(item='', default=None):
    """
    获取某个配置的值

    :param item: 配置项名。如果是多级配置，则以 "/a/b" 的形式提供
    :param default: 默认值（可选）
    :returns: 这个配置的值。如果没有该配置，则提供一个默认值
    """
    global has_init
    if not has_init:
        init()
    if not item:
        return _config
    if item[0] == '/':
        return get_path(item, default)
    try:
        return _config[item]
    except KeyError:
        print("%s not specified in profile, defaulting to '%s'",
                        item, default)
        return default
    
def getConfig():
    """
    返回全部配置数据

    :returns: 全部配置数据（字典类型）
    """
    return _config

def getText():
    if os.path.exists(constants.getConfigPath()):
        with open(constants.getConfigPath(), 'r') as f:
            return f.read()
    return ''

def dump(configStr):
    with open(constants.getConfigPath(), 'w') as f:
        f.write(configStr)        
        