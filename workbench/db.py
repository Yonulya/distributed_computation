import sqlite3

conn = sqlite3.connect("D:/storage.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS mytable (
    item TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()