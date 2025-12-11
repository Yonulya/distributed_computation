from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import datetime
import random

# Function to ping website
def ping_website(url):
    try:
        response = requests.get(url[0], timeout=1)
        is_display = random.randint(0, 1000)
        if is_display >= 0:
            print(f'{datetime.datetime.now().isoformat()} : \t\t {url[0]} \t returned \t {response.status_code}')
        return url[0], response.status_code
    except Exception as e:
        return url[0], str(e)


# Run in parallel using ThreadPoolExecutor
def ping_multiple_websites(urls):
    with ThreadPoolExecutor(max_workers=workers_throttle) as executor:
        results = list(executor.map(ping_website, urls))
    return results

conn = sqlite3.connect("D:/storage.db")
cur = conn.cursor()
cur.execute("PRAGMA journal_mode = WAL")
cur.execute("PRAGMA synchronous = NORMAL")
char_separator = '*'
loop_separator_value = 20
limit = int(1*10**4.7)
workers_throttle = 500 # limit

year = 2025
month = 12
day = 8
hour = 23
minute = 30
end_datetime = datetime.datetime(year, month, day, hour, minute)
# end_datetime = datetime.datetime.now() + datetime.timedelta(seconds=1)

while datetime.datetime.now() < end_datetime:
    
    print(f'{datetime.datetime.now().isoformat()} : Start Select')
    cur.execute(f"SELECT item FROM mytable where value is null limit {limit}")
    urls = cur.fetchall()
    print(f'{datetime.datetime.now().isoformat()} : \t First URL \t= {urls[0][0]}')
    print(f'{datetime.datetime.now().isoformat()} : \t Gotten URL \t= {len(urls)}')
    print(f'{datetime.datetime.now().isoformat()} : \t Last URL \t= {urls[-1][0]}')
    print(f'{datetime.datetime.now().isoformat()} : End Select')
    
    print(f'{datetime.datetime.now().isoformat()} : Start Ping')
    ping_results = ping_multiple_websites(urls)
    print(f'{datetime.datetime.now().isoformat()} : End Ping')

    print(f'{datetime.datetime.now().isoformat()} : Start Update')
    updates = [(status, url) for url, status in ping_results]
    cur.executemany("UPDATE mytable SET value = ? WHERE item = ?", updates)
    conn.commit()
    print(f'{datetime.datetime.now().isoformat()} : End Update')
    print(f'{char_separator}' * loop_separator_value)

print(f'{datetime.datetime.now().isoformat()} : Start Delete')
cur.execute("DELETE FROM mytable where value LIKE ?", ("%Failed to resolve%",))
conn.commit()
print(f'{datetime.datetime.now().isoformat()} : End Delete')