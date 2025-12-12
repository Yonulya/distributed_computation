import sqlite3
import datetime

conn = sqlite3.connect("D:/storage.db")
cur = conn.cursor()
# cur.execute("PRAGMA journal_mode = WAL")
# cur.execute("PRAGMA synchronous = NORMAL")

print(f'{datetime.datetime.now().isoformat()} : Start Delete')
cur.execute("DELETE FROM mytable where value LIKE ?", ("%Failed to resolve%",))
conn.commit()
print(f'{datetime.datetime.now().isoformat()} : End Delete')

print(f'{datetime.datetime.now().isoformat()} Start Vacuum')
cur.execute("VACUUM")
print(f'{datetime.datetime.now().isoformat()} End Vacuum')