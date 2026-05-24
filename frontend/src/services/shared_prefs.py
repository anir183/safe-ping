import logging

import flet as ft
from flet.controls.services.shared_preferences import SharedPreferencesValueType

logger = logging.getLogger(__name__)


async def pref_store(key: str, value: SharedPreferencesValueType) -> None:
	success = False
	try:
		success = await ft.SharedPreferences().set(key, value)
	except Exception:
		logger.error("exception while storing prefs")

	if success:
		logger.info(
			"stored to prefs",
			extra={
				"key": key,
				"value": value,
			},
		)
	else:
		logger.warning(
			"could not store to prefs",
			extra={
				"key": key,
				"value": value,
			},
		)


async def pref_retrieve(key: str) -> SharedPreferencesValueType | None:
	data = None
	try:
		data = await ft.SharedPreferences().get(key)
	except Exception:
		logger.error("exception while retrieving prefs")

	if data is not None:
		logger.info(
			"loaded from prefs",
			extra={
				"key": key,
				"got": data,
			},
		)
	else:
		logger.warning(
			"could not load from prefs",
			extra={
				"key": key,
				"got": data,
			},
		)
	return data
