# -*- coding: utf-8 -*-
from utils.database import Database


def init_permission_db():
    sql = """CREATE TABLE IF NOT EXISTS permissions(
             ID    SERIAL PRIMARY KEY,
             UID   INT NOT NULL,
             LEVEL INT NOT NULL
             );"""
    db = Database()
    cur = db.get_curse()
    cur.execute(sql)
    cur.close()
    db.close_db()
