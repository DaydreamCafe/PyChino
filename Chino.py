# -*- coding: utf-8 -*-
from utils import permissions
from utils.__main__ import Chino

if __name__ == '__main__':
    permissions.init_permission_db()
    bot = Chino()
    bot.run()
