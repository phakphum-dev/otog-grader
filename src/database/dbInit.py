import mysql.connector
from .dbConfig import dbConfig
from constants import bcolors
import time


def init():
    return mysql.connector.connect(**dbConfig)


class DB:
    conn = None

    def connect(self):
        self.conn = init()
        print(bcolors.OKGREEN + 'Mysql: Connection successful.' + bcolors.RESET)

    def disconnect(self):
        self.conn.close()

    def update(self):
        self.conn.commit()

    def query(self, sql, value=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, value)
            return cursor
        except:
            for i in range(5):
                try:
                    self.connect()
                    cursor = self.conn.cursor()
                    cursor.execute(sql, value)
                    return cursor
                except:
                    print(bcolors.WARNING +
                          f'Mysql: Connection Failed, Retrying.. ({i+1})'
                          + bcolors.RESET)
                    time.sleep(i+1)
            print(bcolors.FAIL + 'Mysql: Connection Lost.' + bcolors.RESET)
            exit(1)
