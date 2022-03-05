# -*- coding: utf-8 -*-
import asyncio

from typing import Union

from nonebot import NLPSession, CommandSession
from nonebot.typing import Message_T
from nonebot import logger


class WithdrawMessageSender:
    def __init__(self, session: Union[NLPSession, CommandSession]):
        """
        发送一条自动撤回的消息
        :param session: 聊天session
        """
        self.session = session

    async def send(self, delay_time: float, message: Message_T,):
        """
        发送消息
        :param delay_time: 延迟撤回时间（-1为不撤回）
        :param message: 发送消息内容
        :return: 发送出消息的ID
        """
        msg_id = (await self.session.send(message))['message_id']
        logger.debug(f'已发送延迟撤回消息，id:{msg_id}')
        if delay_time == -1:
            return msg_id
        else:
            await asyncio.sleep(delay_time)
            bot = self.session.bot
            await bot.delete_msg(message_id=msg_id)
            logger.debug(f'已撤回信息，id:{msg_id}')
            return msg_id
