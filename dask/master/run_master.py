"""
Master client script.
- Connects to the Dask scheduler
- Dispatches ping tasks
- Gathers results and writes to SQLite in batches using DBWriter
"""
import argparse
from dask.distributed import Client, as_completed
from db_writer import DBWriter
import time

BATCH_WRITE = 5000

def read_hosts(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main(scheduler, db_path, hosts_path, batch_size=BATCH_WRITE, chunk_size=1000):
    client = Client(scheduler)
    print("Connected to Dask scheduler:", client)

    hosts = read_hosts(hosts_path)

    # Submit tasks in chunks to avoid creating millions of futures
    futures = []
    for i in range(0, len(hosts), chunk_size):
        chunk = hosts[i:i + chunk_size]
        fs = client.map("worker.ping_task.ping_host", chunk)
        futures.extend(fs)

    print(f"Submitted {len(futures)} tasks")

    db = DBWriter(db_path)

    # Gather results as they complete to avoid waiting for all
    completed_batch = []
    for future in as_completed(futures):
        try:
            host, status = future.result()
        except Exception as e:
            host, status = ("<unknown>", f"error:{e}")

        completed_batch.append((host, status))

        if len(completed_batch) >= batch_size:
            print(f"Writing batch of {len(completed_batch)} to DB")
            db.bulk_upsert(completed_batch)
            completed_batch = []

    if completed_batch:
        print(f"Writing final batch of {len(completed_batch)} to DB")
        db.bulk_upsert(completed_batch)

    db.close()
    client.close()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scheduler', required=True)
    ap.add_argument('--db', required=True)
    ap.add_argument('--hosts', required=True)
    ap.add_argument('--batch', type=int, default=BATCH_WRITE)
    ap.add_argument('--chunk', type=int, default=1000)
    args = ap.parse_args()
    main(args.scheduler, args.db, args.hosts, args.batch, args.chunk)