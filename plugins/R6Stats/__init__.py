"""
R6Stats - 一个用于从r6stats查询R6战绩的插件
"""
# -*- coding: utf-8 -*-
import base64

from nonebot import on_command, CommandSession
from nonebot import MessageSegment

from api import config
from api.permissions import check_permission
from utils import config as nonebot_config

from plugins.R6Stats import data_source
from plugins.R6Stats import renderer
from plugins.R6Stats import db

__plugin_name__ = 'R6Stats'
__plugin_usage__ = """
指令：
    查询R6战绩/查R6战绩/查询R6/查R6/R6战绩 <ID> - 查询<ID>玩家R6战绩
    绑定R6账号/关联R6账号/绑定R6/关联R6 <ID> - 将ID为<ID>的R6账号与QQ关联，查询时可不用再次输入ID
    解除绑定R6账号/解除关联R6账号/解除绑定R6/解除关联R6/取消关联R6账号/取消绑定R6/取消关联R6 - 取消QQ与R6账号的关联
""".strip()
__plugin_des__ = "查询R6战绩"
__plugin_cmd__ = ['查询R6战绩', '绑定R6账号', '解除绑定R6账号']
__plugin_version__ = 1.0
__plugin_author__ = "WhitePaper233"

# 读取插件配置
with open('./plugins/R6Stats/config.yaml', 'r', encoding='utf-8') as f:
    config = config.PluginConfig(plugin_name=__plugin_name__, default_config=f).config
# 设置代理，若未设置全局代理则使用插件配置内的代理
# note: aiohttp的proxy参数为空字符串时自动不代理
proxy = nonebot_config.GLOBAL_PROXY if nonebot_config.GLOBAL_PROXY else config['proxy']


# 注册查战绩指令
@on_command('查询R6战绩', aliases=['查R6战绩', '查询R6', '查R6', 'R6战绩', '战绩R6'],
            permission=lambda sender: check_permission(config['level'], sender))
async def _(session: CommandSession):
    game_id = session.current_arg_text.strip()  # 获取游戏ID
    if not game_id:  # 如果没有填写ID
        try:  # 尝试从数据库获取关联的账号
            database = db.StatsR6DB()  # 初始化数据库
            game_id = database.get_linked_account(session.event.user_id)  # 从数据库获取
        except db.AccountNotLinkedError:  # 若没有关联账号，则向用户询问查询ID
            game_id = (await session.aget(prompt='你想查询哪个账号的战绩呢？')).strip()
        while not game_id:
            game_id = (await session.aget(prompt='要查询的账号不能为空呢，请重新输入')).strip()
    try:
        # 尝试获取目标账号数据
        stats_data = await data_source.get_stats(game_id, proxy)
    except IndexError:
        # 没有返回目标数据时提醒用户确认ID
        await session.send('没有找到这个玩家呢~检查下ID是否拼写正确？')
    else:
        # 若正确获取数据
        rendered_img = await renderer.StatsRenderer(stats_data, proxy).render()  # 渲染数据图
        pic_base64 = base64.b64encode(rendered_img.getvalue()).decode()  # 数据图Base64编码
        await session.send(MessageSegment.image('base64://' + pic_base64))  # 发送数据图


# 注册绑定账号指令
@on_command('绑定R6账号', aliases=['关联R6账号', '绑定R6', '关联R6'],
            permission=lambda sender: check_permission(config['level'], sender))
async def _(session: CommandSession):
    # 获取需绑定的ID
    game_id = session.current_arg_text.strip()
    if not game_id:  # 如果用户没有输入ID则向用户询问
        game_id = (await session.aget(prompt='你想绑定哪个账号呢？')).strip()
        while not game_id:
            game_id = (await session.aget(prompt='要绑定的账号不能为空呢，请重新输入')).strip()
    database = db.StatsR6DB()  # 初始化数据库
    try:  # 数据库写入绑定信息
        database.link_account(uid=session.event.user_id, account=game_id)
        await session.send('账号绑定成功！')
    except db.AccountAlreadyLinkedError as error:  # 如果已经绑定
        confirm = (await session.aget(prompt=f'你已经绑定了账号{error.account}, 是否要覆盖绑定？')).strip()
        if confirm in ['是', '确定', '确认', '同意', '继续']:
            database.cancel_link(uid=session.event.user_id)
            database.link_account(uid=session.event.user_id, account=game_id)
            await session.send('账号绑定成功！')
        else:
            await session.send('已取消覆盖绑定！')


# 注册解除绑定命令
@on_command('解除绑定R6账号', aliases=['解除关联R6账号', '解除绑定R6', '解除关联R6', '取消关联R6账号', '取消绑定R6', '取消关联R6'],
            permission=lambda sender: check_permission(config['level'], sender))
async def _(session: CommandSession):
    database = db.StatsR6DB()
    try:  # 尝试解除绑定
        database.cancel_link(session.event.user_id)
        await session.send('解除绑定成功！')
    except db.AccountNotLinkedError:  # 如果没有绑定
        await session.send('你还没有关联R6账号哦！')
