import sqlite3
from pathlib import Path


class DBWriter:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hosts (
                    host TEXT PRIMARY KEY,
                    status TEXT
                )
                """
            )
            conn.commit()

    def write_batch(self, rows: list[tuple[str, str]]):
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                """
                INSERT INTO hosts (host, status)
                VALUES (?, ?)
                ON CONFLICT(host) DO UPDATE SET status=excluded.status
                """,
                rows,
            )
            conn.commit()
