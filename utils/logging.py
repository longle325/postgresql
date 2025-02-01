import sys
import logging
from pathlib import Path


def setup_logging(file_path: Path):
    folder = file_path.parent
    folder.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(str(file_path))
    stream_handler = logging.StreamHandler(sys.stdout)

    # Create formatters and add it to handlers
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%y/%m/%d"
    formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
