from distributed_computation.common.ping import ping_website
from concurrent.futures import ThreadPoolExecutor

# Run in parallel using ThreadPoolExecutor
def ping_multiple_websites_task(urls: list[str]) -> list[tuple[str, str]]:
    with ThreadPoolExecutor(max_workers=min(32, len(urls))) as executor:
        results = list(executor.map(ping_website, urls))
    return results