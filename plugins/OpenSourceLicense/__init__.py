"""
开源软件许可插件 - 用于发送一条开源软件许可详情消息
"""
# -*- coding: utf-8 -*-
from nonebot import on_command, CommandSession

from api.permissions import check_permission

__plugin_name__ = 'OpenSourceLicense'
__plugin_usage__ = """
指令：
    开源软件许可 - 显示开源软件许可详情消息
""".strip()
__plugin_des__ = "显示开源软件许可详情消息"
__plugin_cmd__ = ['开源软件许可']
__plugin_version__ = 1.0
__plugin_author__ = "WhitePaper233"


@on_command('开源软件许可', permission=lambda sender: check_permission(0, sender))
async def _(session: CommandSession):
    msg = """开源软件许可表:
------------
Chino: 服务型机器人
Author: DaydreamCafe (DaydreamCafé)
License: AGPL-3.0 License
Repo: https://github.com/DaydreamCafe/Chino
------------
nonebot: Asynchronous QQ robot framework based on OneBot for Python
Author: nonebot (NoneBot)
License: MIT License
Repo: https://github.com/nonebot/nonebot
------------
PyYAML: A full-featured YAML processing framework for Python
Author: yaml (The YAML Project)
License: MIT License
Repo: https://github.com/yaml/pyyaml
------------
psycopg2: PostgreSQL database adapter for the Python programming language
Author: psycopg (The Psycopg Team)
License: GNU Lesser General Public License
Repo: https://github.com/psycopg/psycopg2
------------
requests: A simple, yet elegant, HTTP library.
Author: psf (Python Software Foundation)
License: Apache-2.0 License
Repo: https://github.com/psf/requests
------------
aiohttp: Asynchronous HTTP client/server framework for asyncio and Python
Author: aio-libs (aio-libs)
License: Apache-2.0 License
Repo: https://github.com/aio-libs/aiohttp
------------
Pillow: The friendly PIL fork (Python Imaging Library)
Author: python-pillow (Pillow)
License: HPND License
Repo: https://github.com/python-pillow/Pillow
"""
    await session.send(msg)
