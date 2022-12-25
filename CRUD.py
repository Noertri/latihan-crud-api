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

    def __init__(self, database):
        try:
            self.database = database
            self.connection = sqlite3.connect(database=database, timeout=20)
            self.connection.row_factory = self.dict_factory
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error(f"{e}", exc_info=True)

    @staticmethod
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    @property
    def column_names(self):
        return self.cursor.description

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            logger.error(f"{e}", exc_info=True)

    def close(self):
        try:
            self.connection.close()
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
