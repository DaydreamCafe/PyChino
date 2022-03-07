# -*- coding: utf-8 -*-
import re

import yaml

from pathlib import Path

from nonebot.default_config import *

# 读取配置文件
with open('./config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# 地址端口
HOST = config['host']
PORT = config['port']

# 全局代理
GLOBAL_PROXY = config['proxy']

# 别名
NICKNAME = config['nicknames']

# 超级管理员
SUPERUSERS = config['super_users']

# 命令匹配
command_prefix = ''
for i in config['command_prefix']:
    command_prefix += i
if config['no_prefix']:
    COMMAND_START = ['', re.compile(rf'[{command_prefix}]+')]
else:
    COMMAND_START = [re.compile(rf'[{command_prefix}]+')]

# 默认权限
DEFAULT_PERMISSION = config['default_permission']

# 图片路径
IMAGE_PATH = Path() / "resources" / "image"

# 调试设置
DEBUG = config['debug']
