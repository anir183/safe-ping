import logging

import flet as ft
from flet.controls.services.shared_preferences import SharedPreferencesValueType

logger = logging.getLogger(__name__)

_service = ft.SharedPreferences()


async def store(key: str, value: SharedPreferencesValueType) -> None:
	success = await _service.set(key, value)
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


async def retrieve(key: str) -> SharedPreferencesValueType | None:
	data = await _service.get(key)
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
