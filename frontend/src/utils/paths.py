import os
from pathlib import Path

from platformdirs import user_log_dir

from constants.info import APP_VERSION
from constants.utils import (
	ENV_ASSETS_DIR,
	PATHS_ASSET_DIR,
	PATHS_DEV_ROOT_DEPTH,
	PATHS_LOG_DIR,
	PATHS_LOG_DIR_APP_AUTHOR,
	PATHS_LOG_DIR_APP_NAME,
	PATHS_LOG_FILE_NAME,
	PATHS_ROOT_RESOLUTION_FILE,
)


def get_dev_root() -> Path | None:
	dev_root = Path(__file__).resolve()

	depth = PATHS_DEV_ROOT_DEPTH
	while not (dev_root / PATHS_ROOT_RESOLUTION_FILE).exists() and depth > 0:
		dev_root = dev_root.parent
		depth -= 1

	return (dev_root / PATHS_ROOT_RESOLUTION_FILE).exists() and dev_root or None


def get_logs_dir() -> Path:
	dev_root = get_dev_root()

	if dev_root:
		log_dir = dev_root / PATHS_LOG_DIR
	else:
		log_dir = Path(
			user_log_dir(
				appname=PATHS_LOG_DIR_APP_NAME,
				appauthor=PATHS_LOG_DIR_APP_AUTHOR,
				version=APP_VERSION,
			)
		).resolve()

	log_dir.mkdir(
		parents=True,
		exist_ok=True,
	)

	return log_dir


def get_log_file() -> Path:
	return get_logs_dir() / PATHS_LOG_FILE_NAME


def get_asset_dir() -> Path:
	env_assets = os.getenv(ENV_ASSETS_DIR)
	dev_root = get_dev_root()
	dev_assets = None

	if dev_root:
		dev_assets = (dev_root / PATHS_ASSET_DIR).resolve()

	if env_assets and (dev_assets and not dev_assets.exists()):
		return Path(env_assets).resolve()

	assert dev_assets, f"{__name__}: dev assets directory is None"
	return dev_assets


def get_asset_path(rel_path: Path) -> Path:
	return get_asset_dir() / rel_path
