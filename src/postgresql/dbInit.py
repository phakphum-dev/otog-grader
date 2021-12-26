import traceback
import psycopg

from constants.colors import colors
from .dbConfig import dbConfig


def init():
    return psycopg.connect(**dbConfig)


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
            cursor = self.conn.cursor()
            cursor.execute(sql, value)
            return cursor
        except Exception:
            print(
                f"{colors.WARNING}[ PostgreSQL ]{colors.RESET} Execute failed."
            )
            traceback.print_exc()
            return None
