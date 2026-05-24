import json
import logging
from logging.handlers import RotatingFileHandler
from typing import final, override

from constants.utils import (
	LOG_FILE_ENCODING,
	LOG_FILE_MAX_BACKUPS,
	LOG_FILE_MAX_BYTES,
	LOG_IGNORE_KEYS,
	LOG_JSON_INDENT,
)
from utils.paths import get_log_file


@final
class ExtrasFormatter(logging.Formatter):
	@override
	def format(self, record: logging.LogRecord) -> str:
		extras = {
			key: value
			for key, value in record.__dict__.items()
			if key not in LOG_IGNORE_KEYS
		}

		base = super().format(record)

		if not extras:
			return base

		try:
			extra_json = json.dumps(
				extras,
				default=str,
				indent=LOG_JSON_INDENT,
			)
		except Exception:
			extra_json = str(extras)

		return f"{base}\n{extra_json}"


def setup_logging():
	formatter = ExtrasFormatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)

	log_file = get_log_file()

	file_handler = RotatingFileHandler(
		log_file,
		maxBytes=LOG_FILE_MAX_BYTES,
		backupCount=LOG_FILE_MAX_BACKUPS,
		encoding=LOG_FILE_ENCODING,
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

	logging.getLogger(__name__).info(
		"logging initialized",
		extra={
			"log_file": str(log_file),
		},
	)
