import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(processName)s | "
    "%(threadName)s | "
    "%(name)s | "
    "%(message)s"
)

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )