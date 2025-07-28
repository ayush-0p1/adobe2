import logging, os

def get_logger(name: str):
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format="[%(levelname)s] %(message)s")
    return logging.getLogger(name)
