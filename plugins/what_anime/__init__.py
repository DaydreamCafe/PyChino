"""
what_anime - 一个用于根据图片查询番剧的插件
"""
# -*- coding: utf-8 -*-
from api import config
from utils import config as nonebot_config
from api.permissions import check_permission

from nonebot import on_command, CommandSession

from plugins.what_anime import data_source

__plugin_name__ = 'what_anime'
__plugin_usage__ = """
指令：
    识别番剧图片/识别番剧/识番 <番剧图片> - 根据图片查询番剧名称
""".strip()
__plugin_des__ = "根据图片查询番剧"
__plugin_cmd__ = ['识别番剧图片', '识别番剧', '识番']
__plugin_version__ = 1.0
__plugin_author__ = "WhitePaper233"

# 读取插件配置
with open('./plugins/what_anime/config.yaml', 'r', encoding='utf-8') as f:
    config = config.PluginConfig(plugin_name=__plugin_name__, default_config=f).config
# 设置代理，若未设置全局代理则使用插件配置内的代理
# note: aiohttp的proxy参数为空字符串时自动不代理
proxy = nonebot_config.GLOBAL_PROXY if nonebot_config.GLOBAL_PROXY else config['proxy']


@on_command('识别番剧图片', aliases=['识别番剧', '识番'],
            permission=lambda sender: check_permission(config['level'], sender))
async def _(session: CommandSession):
    pic_url = session.current_arg_images
    if len(pic_url) > 1:
        await session.send('给的图片太多啦！智乃酱处理不过来啦！请只给一张图片！')
    elif not pic_url:
        await session.send('图呢？没图怎么查？')
    else:
        await session.send(await data_source.TraceMeo(pic_url[0]).get_result_formatted(proxy))
