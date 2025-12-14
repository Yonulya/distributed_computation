import sqlite3
from pathlib import Path
import sqlite3

class DBClass:
    def __init__(self, db_path: str):
        db_path = Path(db_path)
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS mytable (
                item TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        self.conn.commit()

    def write_batch(self, updates: list[tuple[str, str]]):
        self.cur.executemany("UPDATE mytable SET value = ? WHERE item = ?", updates)
        self.conn.commit()
        print(f'Wrote {len((updates))} updates')

    def load_hosts(self, limit: int) -> list[str]:
        self.cur.execute("SELECT item FROM mytable WHERE value IS NULL LIMIT ?",(limit,))
        urls = [row[0] for row in self.cur]
    
        return urls