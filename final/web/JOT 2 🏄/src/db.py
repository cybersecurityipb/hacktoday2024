import sqlite3


class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self._con = sqlite3.connect(f"databases/{self.dbname}")
        self.cursor = self._con.cursor
        self.commit = self._con.commit
        self.close = self._con.close
        self._initdb()

    def _initdb(self):
        con = sqlite3.connect(f"databases/{self.dbname}")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                verified TEXT NOT NULL
            );"""
        )
        cur.close()
        con.commit()
        con.close()
        del con, cur

    def __del__(self):
        self._con.close()

if __name__ == "__main__":
    db = Database("database.db")
    db.close()
    del db
