from __future__ import annotations

import logging
from pathlib import Path


LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "logs.log"


def configure_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    root_logger = logging.getLogger("sysmon")
    if root_logger.handlers:
        return

    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)


def get_logger() -> logging.Logger:
    configure_logging()
    return logging.getLogger("sysmon")


def logger() -> None:
    configure_logging()


if __name__ == "__main__":
    configure_logging()
    get_logger().info("Logger is configured and ready.")
    print(f"Log file created at: {LOG_PATH}")
