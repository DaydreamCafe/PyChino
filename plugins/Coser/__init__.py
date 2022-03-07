"""
Coser插件 - 发送一张coser图片
"""
# -*- coding: utf-8 -*-
import requests
from nonebot import on_natural_language, NLPSession

from api import config
from api.session import withdraw_message_sender
from api.permissions import check_permission
from utils import config as nonebot_config

__plugin_name__ = 'Coser'
__plugin_usage__ = """
指令：
    cos/coser - 返回一张coser图片
""".strip()
__plugin_des__ = "三次元也不戳，嘿嘿嘿（流鼻血"
__plugin_cmd__ = ['cos', 'coser']
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier / WhitePaper233"

with open('./plugins/Coser/config.yaml', 'r', encoding='utf-8') as f:
    config = config.PluginConfig(plugin_name=__plugin_name__, default_config=f).config
# 设置代理，若未设置全局代理则使用插件配置内的代理
# note: aiohttp的proxy参数为空字符串时自动不代理
proxy = {'https': nonebot_config.GLOBAL_PROXY} if nonebot_config.GLOBAL_PROXY else {}

if config['limit_superuser']:
    config['level'] = 10


@on_natural_language(keywords=__plugin_cmd__, permission=lambda sender: check_permission(config['level'], sender))
async def _(session: NLPSession):
    message_session = withdraw_message_sender.WithdrawMessageSender(session)
    if proxy:
        resp = requests.get('https://api.iyk0.com/cos', proxies=proxy)
    else:
        resp = requests.get('https://api.iyk0.com/cos')
    await message_session.send(config['withdraw_time'], f'[CQ:image,file=coser,url={resp.url}]')
