import argparse
from dask.distributed import Client

from distributed_computation.worker.tasks import ping_task
from distributed_computation.master.db_writer import DBWriter


def load_hosts(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main(scheduler: str, db_path: str, hosts_file: str, batch_size: int):
    client = Client(scheduler)
    print("Connected to Dask:", client)

    hosts = load_hosts(hosts_file)
    writer = DBWriter(db_path)

    futures = client.map(ping_task, hosts)

    batch = []
    for future in futures:
        batch.append(future.result())

        if len(batch) >= batch_size:
            writer.write_batch(batch)
            batch.clear()

    if batch:
        writer.write_batch(batch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheduler", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--hosts", required=True)
    parser.add_argument("--batch-size", type=int, default=100)

    args = parser.parse_args()

    main(
        scheduler=args.scheduler,
        db_path=args.db,
        hosts_file=args.hosts,
        batch_size=args.batch_size,
    )
