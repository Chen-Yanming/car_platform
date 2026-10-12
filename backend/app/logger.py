import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "register.log"


def get_register_logger() -> logging.Logger:
  logger = logging.getLogger("register")
  if logger.handlers:
    return logger

  handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5, delay=False)
  formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
  )
  handler.setFormatter(formatter)

  logger.setLevel(logging.INFO)
  logger.addHandler(handler)
  return logger

