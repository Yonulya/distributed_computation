import random
from distributed.worker import get_worker
import logging
from concurrent.futures import ThreadPoolExecutor

from distributed_computation.common.ping import ping_website
from distributed_computation.common.logging_config import setup_logging

SAMPLE_RATE = 0.01

setup_logging()
logger = logging.getLogger(__name__)

# Run in parallel using ThreadPoolExecutor
def ping_multiple_websites_task(urls: list[str], max_workers: int) -> list[tuple[str, str]]:
    worker = get_worker()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(ping_website, urls))
    
    for url, status in results:
        if random.random() < SAMPLE_RATE:
            logger.info("Ping result: %s -> %s", url, status)

    return results