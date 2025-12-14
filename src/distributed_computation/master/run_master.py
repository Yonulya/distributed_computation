import argparse
from dask.distributed import Client

from distributed_computation.worker.tasks import ping_multiple_websites_task
from distributed_computation.master.db_class import DBClass


def main(scheduler: str, db_path: str, limit: int, batch_size: int, chunk: str):
    client = Client(scheduler)
    print("Connected to Dask:", client)

    db = DBClass(db_path)
    hosts = db.load_hosts(limit)
    
    futures = client.map(ping_multiple_websites_task, hosts, chunk)

    batch = []
    updates = []
    for future in futures:
        batch.append(future.result())
        
        updates = [(status, url) for url, status in batch]
        if len(updates) >= batch_size:
            db.write_updates(updates)
            batch.clear()

    if batch:
        db.write_updates(updates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheduler", required=True)
    # parser.add_argument("--db", required=True)
    # parser.add_argument("--hosts", required=True)
    # parser.add_argument("--batch-size", type=int, default=5000)

    args = parser.parse_args()

    # main(
    #     scheduler=args.scheduler,
    #     db_path=args.db,
    #     hosts_file=args.hosts,
    #     batch_size=args.batch_size,
    # )

    main(
        scheduler=args.scheduler,
        db_path="D:/storage.db",
        limit=5000,#int(1*10**4.7),
        batch_size=1000,
        chunk="500"
    )