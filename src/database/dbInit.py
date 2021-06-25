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
        return

    def disconnect(self):
        self.conn.close()

    def update(self):
        self.conn.commit()

    def query(self, sql, value=()):
        try:
            cursor = self.conn.cursor(buffered=True)
            cursor.execute(sql, value)
            return cursor
        except:
            for i in range(5):
                try:
                    print(
                        f"{bcolors.WARNING}[ MYSQL ] Connection failed, retrying in ({i+1}) secs...{bcolors.RESET}"
                    )
                    time.sleep(i + 1)
                    self.connect()
                    print(
                        f"{bcolors.OKGREEN}[ MYSQL ] Connect MYSQL success fully!.{bcolors.RESET}")
                    cursor = self.conn.cursor(buffered=True)
                    cursor.execute(sql, value)
                    return cursor
                except:
                    pass
            print(f"{bcolors.FAIL}[ MYSQL ] Connection Lost.{bcolors.RESET}")
            exit(1)
