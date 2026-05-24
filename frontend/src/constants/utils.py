LOG_IGNORE_KEYS = frozenset(
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

LOG_JSON_INDENT = 4

LOG_FILE_MAX_BYTES = 5_000_000
LOG_FILE_MAX_BACKUPS = 5
LOG_FILE_ENCODING = "utf-8"

APP_VERSION = "30ef264623"

PATHS_DEV_ROOT_DEPTH = 5
PATHS_ROOT_RESOLUTION_FILE = "pyproject.toml"
PATHS_ASSET_DIR = "assets"
PATHS_LOG_DIR = "logs"
PATHS_LOG_FILE_NAME = "app.log"
PATHS_LOG_DIR_APP_NAME = "safe-ping"
PATHS_LOG_DIR_APP_AUTHOR = "anir183"

ENV_ASSETS_DIR = "FLET_ASSETS_DIR"
