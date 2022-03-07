# -*- coding: utf-8 -*-
from nonebot import SenderRoles

from utils import config
from utils.database import Database


def if_superuser(uid: int) -> bool:
    return uid in config.SUPERUSERS


def get_permission(uid: int) -> int:
    db = Database()
    cur = db.get_curse()
    cur.execute(f'SELECT uid, level FROM permissions WHERE UID = {uid};')
    result = cur.fetchone()
    cur.close()
    db.close_db()
    if result is None:
        return config.DEFAULT_PERMISSION
    else:
        return result[1]


async def check_permission(level: int, sender: SenderRoles, callback=None):
    uid = sender.event.user_id
    if callback is not None and (not if_superuser(uid) or not get_permission(uid) >= level):
        await callback()
    return True if if_superuser(uid) or get_permission(uid) >= level else False
