import argparse
from dask.distributed import Client, as_completed

from distributed_computation.worker.tasks import ping_multiple_websites_task
from distributed_computation.master.db_class import DBClass

def main(scheduler: str, db_path: str, limit: int, chunk_size: int):
    client = Client(scheduler)
    print("Connected to Dask:", client)

    db = DBClass(db_path)
    hosts = db.load_hosts(limit)
    futures = []
    for i in range(0, len(hosts), chunk_size):
        hosts_chunked = hosts[i:i + chunk_size]
        fs = client.submit(ping_multiple_websites_task, hosts_chunked)
        futures.append(fs)

    try:
        for future in as_completed(futures):
            updates = [(status, url) for url, status in future.result()]
            db.write_batch(updates)
    except KeyboardInterrupt:
        print("⚠️ Shutdown requested — cancelling remaining tasks")
        client.cancel(futures)
    finally:
        client.close()


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
        limit=int(1*10**5),
        chunk_size=200
    )