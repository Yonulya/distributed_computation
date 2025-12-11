import itertools
import string
import sqlite3

def brute_force_strings(min_len=1, max_len=12, alphabet=string.ascii_lowercase):
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(alphabet, repeat=length):
            yield "".join(combo)


list_top_level_domain = [".com", ".net", ".org"]
batch = []

conn = sqlite3.connect("D:/storage.db")
cur = conn.cursor()
cur.execute("PRAGMA journal_mode = WAL")
cur.execute("PRAGMA synchronous = NORMAL")

for domain in brute_force_strings(6, 6):
    urls = ['https://www.' + domain + top_level_domain for top_level_domain in list_top_level_domain]
    for url in urls:
        batch.append((url, None))
    
    if len(batch) > 950000 and len(batch) < 1000000:  # every 100k
        print("in")
        cur.executemany("INSERT OR IGNORE INTO mytable (item, value) VALUES (?, ?)", batch)
        conn.commit()
        batch = []