from distributed_computation.common.ping import ping_website
from concurrent.futures import ThreadPoolExecutor

# Run in parallel using ThreadPoolExecutor
def ping_multiple_websites_task(urls: str, workers_throttle: str) -> list[tuple[str, str]]:
    with ThreadPoolExecutor(max_workers=workers_throttle) as executor:
        results = list(executor.map(ping_website, urls))
    return results