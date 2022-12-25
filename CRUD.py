"""Modul CRUD (Create, Read, Update, Delete) untuk menangani database"""

import sqlite3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.ERROR)
fmtr = logging.Formatter("%(asctime)s: [%(levelname)s] %(message)s")
stream_handler.setFormatter(fmtr)
logger.addHandler(stream_handler)


class SqliteDB:
    cursor = None
    database = None
    conn = None

    def __init__(self, database):
        try:
            self.conn = sqlite3.connect(database=database)
            self.conn.row_factory = self.dict_factory
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"{e}", exc_info=True)

    @staticmethod
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def create(self, tablename, columns):
        sql = """CREATE TABLE IF NOT EXISTS {0} ({1});""".format(tablename, columns)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.error(f"{e}", exc_info=True)

    def insert(self, tablename, **records):
        sql = "INSERT INTO {0} ({1}) VALUES ({2});".format(tablename, ", ".join(records.keys()), ", ".join(["?" for _ in range(len(records))]))
        self.cursor.execute(sql, [v for v in records.values()])
        self.conn.commit()
        return True

    def check_duplicate(self, tablename, record):
        sql = "SELECT COUNT(*) FROM {0} WHERE judul=? AND url=?;".format(tablename)
        self.cursor.execute(sql, (record["judul"], record["url"]))
        count = self.cursor.fetchone()

        if count[0] == 0:
            return True
        else:
            return False

    def query_all(self, tablename):
        sql = "SELECT * FROM {0}".format(tablename)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as err:
            logger.error(f"{err}", exc_info=True)
            return None

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as sqerr:
            logging.error(f"{sqerr}", exc_info=True)
        except Exception as err:
            logger.error(f"{err}", exc_info=True)
