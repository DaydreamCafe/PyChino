# -*- coding: utf-8 -*-
import yaml
import psycopg2


class Database:
    def __init__(self):
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)['db']
        self.conn = psycopg2.connect(
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'])

    def get_curse(self):
        return self.conn.cursor()


if __name__ == '__main__':
    cur = Database().conn.cursor()
    cur.execute('SELECT version()')
    print(cur.fetchone())
