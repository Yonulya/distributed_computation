from distributed_computation.common.ping import ping_host


def ping_task(host: str) -> tuple[str, str]:
    """
    Dask worker task.
    """
    host, ok = ping_host(host)
    status = "up" if ok else "down"
    return host, status
