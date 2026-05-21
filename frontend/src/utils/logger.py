import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def setup_logging():
	formatter = logging.Formatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)

	file_handler = RotatingFileHandler(
		LOG_FILE,
		maxBytes=5_000_000,
		backupCount=10,
		encoding="utf-8",
	)

	file_handler.setFormatter(formatter)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(formatter)

	logging.basicConfig(
		level=logging.INFO,
		handlers=[
			file_handler,
			console_handler,
		],
	)
