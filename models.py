"""Modul untuk menangani CRUD (Create, Read, Update, Delete) database"""

import sqlite3


class DatabaseMahasiswa:

    def __init__(self, database):
        try:
            self.database = database
            self.connection = sqlite3.connect(database=database, timeout=20)
            self.connection.row_factory = self.dict_factory
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e

    @staticmethod
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    @property
    def column_names(self):
        return self.cursor.description

    def insert(self, tablename, record):
        _sql = "INSERT INTO {0} ({1}) VALUES ({2});".format(tablename, ", ".join(record.keys()), ", ".join(["?" for _ in range(len(record))]))
        _sql2 = "SELECT COUNT(*) AS c FROM {0} WHERE nama=? AND nim=? AND jurusan=?;".format(tablename)
        self.cursor.execute(_sql2, [v.strip() for v in record.values()])
        count = self.cursor.fetchone()
        if count["c"] == 0:
            try:
                self.cursor.execute(_sql, [v.strip() for v in record.values()])
                self.commit()
            except Exception as e:
                raise e
        else:
            raise ValueError("Nilai sudah ada!!!")

    def query_all(self, tablename):
        _sql = "SELECT * FROM {0}".format(tablename)
        try:
            self.cursor.execute(_sql)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def query_by_id(self, tablename, _id):
        _sql = "SELECT id FROM {0} WHERE id = ?;".format(tablename)
        try:
            self.cursor.execute(_sql, (_id,))
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def update(self):
        pass

    def delete_by_id(self, tablename, _id):
        _sql = "DELETE FROM {0} WHERE id=?;".format(tablename)
        _sql2 = "SELECT COUNT(id) AS c FROM {0} WHERE id=?;".format(tablename)
        self.cursor.execute(_sql2, (_id,))
        count = self.cursor.fetchone()
        if count["c"] > 0:
            try:
                self.cursor.execute(_sql, (_id,))
                self.commit()
            except Exception as e:
                raise e
        else:
            raise ValueError(f"id dengan nilai {_id} tidak ada!!!")

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            raise e

    def close(self):
        try:
            self.connection.close()
        except Exception as e:
            raise e
