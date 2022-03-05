# -*- coding: utf-8 -*-
import nonebot

from utils import config


class Chino:
    @staticmethod
    def run():
        nonebot.init(config)
        nonebot.load_plugins('./plugins', 'plugins')
        nonebot.run()
