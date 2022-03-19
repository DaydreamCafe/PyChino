# -*- coding: utf-8 -*-
import os

import nonebot

from utils import config


class Chino:
    @staticmethod
    def run():
        nonebot.init(config)
        nonebot.log.logger.info(f'Chino Bot is running at PID: {os.getpid()}')
        nonebot.load_plugins('./plugins', 'plugins')
        nonebot.run()
