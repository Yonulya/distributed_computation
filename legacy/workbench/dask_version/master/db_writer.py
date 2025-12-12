"""
Database helper for batched inserts/updates into SQLite.
All DB writes must be performed from the master only.
"""
import sqlite3
from typing import Iterable, Tuple

DEFAULT_PRAGMAS = [
    ("journal_mode", "WAL"),
    ("synchronous", "NORMAL"),
]

class DBWriter:
    def __init__(self, path: str, pragmas=None):
        self.path = path
        self.pragmas = pragmas or DEFAULT_PRAGMAS
        self.conn = sqlite3.connect(self.path, timeout=1)
        self.cur = self.conn.cursor()
        self._apply_pragmas()
        self._ensure_table()

    def _apply_pragmas(self):
        for key, val in self.pragmas:
            self.cur.execute(f"PRAGMA {key} = {val}")
        self.conn.commit()

    def _ensure_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS hosts (
                hostname TEXT PRIMARY KEY,
                status TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def bulk_upsert(self, rows: Iterable[Tuple[str, str]], batch_size: int = 5000):
        """
        rows: iterable of (hostname, status)
        We'll convert to (status, hostname) for UPDATE param order when needed.
        This method uses executemany in batches for speed.
        """
        batch = []
        insert_sql = "INSERT OR IGNORE INTO hosts (hostname, status) VALUES (?, ?)"
        update_sql = "UPDATE hosts SET status = ?, last_seen = CURRENT_TIMESTAMP WHERE hostname = ?"

        for hostname, status in rows:
            batch.append((hostname, status))
            if len(batch) >= batch_size:
                # Insert missing keys
                self.cur.executemany(insert_sql, batch)
                # Update their status
                update_params = [(s, h) for h, s in batch]
                self.cur.executemany(update_sql, update_params)
                self.conn.commit()
                batch = []

        if batch:
            self.cur.executemany(insert_sql, batch)
            update_params = [(s, h) for h, s in batch]
            self.cur.executemany(update_sql, update_params)
            self.conn.commit()

    def close(self):
        self.conn.close()