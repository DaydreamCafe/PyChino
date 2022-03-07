"""
操作数据库的模块
"""
# -*- coding: utf-8 -*-
from utils import database


class AccountAlreadyLinkedError(Exception):
    def __init__(self, account: str):
        self.account = account

    def __str__(self):
        return f'该QQ已和R6账户{self.account}关联'


class AccountNotLinkedError(Exception):
    def __str__(self):
        return '该QQ未和任何R6账户关联'


class StatsR6DB:
    def __init__(self):
        self.db = database.Database
        db = self.db()
        cur = db.get_curse()
        init_table_sql = """CREATE TABLE IF NOT EXISTS r6stats(
                            UID            INT  NOT NULL,
                            LINKED_ACCOUNT TEXT NOT NULL
                            );"""
        cur.execute(init_table_sql)
        cur.close()
        db.close_db()
        
    def link_account(self, uid: int, account: str):
        db = self.db()
        cur = db.get_curse()
        cur.execute(f'SELECT LINKED_ACCOUNT FROM r6stats WHERE UID = {uid};')
        result = cur.fetchone()
        cur.close()
        if result is not None:
            raise AccountAlreadyLinkedError(result[0])
        cur = db.get_curse()
        sql = f"INSERT INTO r6stats (UID, LINKED_ACCOUNT) VALUES ({uid}, '{account}');"
        cur.execute(sql)
        cur.close()
        db.close_db()

    def cancel_link(self, uid: int):
        db = self.db()
        cur = db.get_curse()
        cur.execute(f'SELECT LINKED_ACCOUNT FROM r6stats WHERE UID = {uid};')
        result = cur.fetchone()
        cur.close()
        if result is None:
            raise AccountNotLinkedError()
        cur = db.get_curse()
        cur.execute(f"DELETE FROM r6stats WHERE uid = {uid}")
        cur.close()
        db.close_db()

    def get_linked_account(self, uid: int):
        db = self.db()
        cur = db.get_curse()
        cur.execute(f'SELECT LINKED_ACCOUNT FROM r6stats WHERE UID = {uid};')
        result = cur.fetchone()
        cur.close()
        db.close_db()
        if result is None:
            raise AccountNotLinkedError()
        else:
            return result[0]
