import sqlite3
import datetime

conn = sqlite3.connect("D:/storage.db")
cur = conn.cursor()
# cur.execute("PRAGMA journal_mode = WAL")
# cur.execute("PRAGMA synchronous = NORMAL")

# cur.execute("SELECT substr(value, 1, 20) as value, count(*) as count FROM mytable where value is not null group by substr(value, 1, 20)")
cur.execute("SELECT * FROM mytable where value is not null order by random() limit 10")

results = cur.fetchall()

for result in results:
    print(result[0])