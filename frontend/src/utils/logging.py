import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import final, override

from platformdirs import user_log_dir

from constants.utils import UtilConsts


@final
class ExtrasFormatter(logging.Formatter):
	@override
	def format(self, record: logging.LogRecord) -> str:
		extras = {
			key: value
			for key, value in record.__dict__.items()
			if key not in UtilConsts.LOG_IGNORE_KEYS
		}

		base = super().format(record)

		if not extras:
			return base

		try:
			extra_json = json.dumps(
				extras,
				default=str,
				indent=UtilConsts.LOG_JSON_INDENT,
			)
		except Exception:
			extra_json = str(extras)

		return f"{base}\n{extra_json}"


def setupLogging():
	formatter = ExtrasFormatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)

	log_dir = Path(
		user_log_dir(
			appname=UtilConsts.LOG_DIR_APP_NAME,
			appauthor=UtilConsts.LOG_DIR_APP_AUTHOR,
			version=UtilConsts.APP_VERSION,
		)
	)

	log_dir.mkdir(
		parents=True,
		exist_ok=True,
	)

	log_file = log_dir / UtilConsts.LOG_FILE_NAME

	file_handler = RotatingFileHandler(
		log_file,
		maxBytes=UtilConsts.LOG_FILE_MAX_BYTES,
		backupCount=UtilConsts.LOG_FILE_MAX_BACKUPS,
		encoding=UtilConsts.LOG_FILE_ENCODING,
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
