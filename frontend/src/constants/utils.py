class UtilConsts:
	LOG_IGNORE_KEYS: frozenset[str] = frozenset(
		{
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
			"taskName",
			"message",
			"asctime",
		}
	)

	LOG_JSON_INDENT: int = 4

	LOG_FILE_MAX_BYTES: int = 5_000_000
	LOG_FILE_MAX_BACKUPS: int = 5
	LOG_FILE_ENCODING: str = "utf-8"

	APP_VERSION: str = "30ef264623"

	PATHS_DEV_ROOT_DEPTH: int = 5
	PATHS_ROOT_RESOLUTION_FILE: str = "pyproject.toml"
	PATHS_ASSET_DIR: str = "assets"
	PATHS_LOG_DIR: str = "logs"
	PATHS_LOG_FILE_NAME: str = "app.log"
	PATHS_LOG_DIR_APP_NAME: str = "safe-ping"
	PATHS_LOG_DIR_APP_AUTHOR: str = "anir183"

	ENV_ASSETS_DIR: str = "FLET_ASSETS_DIR"
