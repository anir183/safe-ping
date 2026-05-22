import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import final, override

BASE_DIR = Path(__file__).resolve().parents[2]

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


@final
class ExtraFormatter(logging.Formatter):
	# ignore these while printing logs
	RESERVED = {
		"name",
		"msg",
		"args",
		"levelname",
		"levelno",
		"pathname",
		"filename",
		"module",
		"exc_info",
		"exc_text",
		"stack_info",
		"lineno",
		"funcName",
		"created",
		"msecs",
		"relativeCreated",
		"thread",
		"threadName",
		"processName",
		"process",
		"message",
		"asctime",
		"taskName",
		"extras",
	}

	@override
	def format(self, record: logging.LogRecord) -> str:
		extras = {
			key: value
			for key, value in record.__dict__.items()
			if key not in self.RESERVED
		}

		base = super().format(record)

		if not extras:
			return base

		try:
			extra_json = json.dumps(
				extras,
				default=str,
				indent=2,
			)

		except Exception:
			extra_json = str(extras)

		return f"{base}\n{extra_json}"


def setup_logging():

	formatter = ExtraFormatter(
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
		force=True,
	)
