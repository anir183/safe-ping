import logging

import flet as ft
from flet.controls.services.shared_preferences import SharedPreferencesValueType

logger = logging.getLogger(__name__)


async def pref_store(key: str, value: SharedPreferencesValueType) -> None:
	success = await ft.SharedPreferences().set(key, value)
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
	data = await ft.SharedPreferences().get(key)
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
