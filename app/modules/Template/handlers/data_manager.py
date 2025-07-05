import sqlite3
import os
from .. import MODULE_NAME


class DataManager:
    def __init__(self):
        data_dir = os.path.join("data", MODULE_NAME)
        os.makedirs(data_dir, exist_ok=True)
        db_path = os.path.join(data_dir, f"data.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """建表函数，如果表不存在则创建"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS""")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    # 其他函数，可直接使用,在with语句块中使用
    def add_data(self, data):
        self.cursor.execute("INSERT INTO data_table (data) VALUES (?)", (data,))
        self.conn.commit()

    def get_data(self):
        self.cursor.execute("SELECT data FROM data_table")
        return self.cursor.fetchall()
