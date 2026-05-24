import asyncio
import logging
from dataclasses import dataclass

import flet as ft

from constants.colors import COLOR_PRIMARY_DARK, COLOR_PRIMARY_LIGHT
from constants.prefs import PREF_THEME_MODE
from services.shared_prefs import pref_retrieve, pref_store

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
	route: str

	theme_mode: ft.ThemeMode = ft.ThemeMode.DARK
	theme_color: ft.Colors = COLOR_PRIMARY_DARK

	async def load_theme(self):
		mode = await pref_retrieve(PREF_THEME_MODE)

		logger.info(
			"loaded stored theme",
			extra={"stored": mode},
		)

		if mode == ft.ThemeMode.LIGHT.value:
			self.theme_mode = ft.ThemeMode.LIGHT
			self.theme_color = COLOR_PRIMARY_LIGHT
		else:
			self.theme_mode = ft.ThemeMode.DARK
			self.theme_color = COLOR_PRIMARY_DARK

	__saving_task = None
	def toggle_theme(self):
		if self.__saving_task and not self.__saving_task.done():
			return

		if self.theme_mode == ft.ThemeMode.LIGHT:
			self.theme_mode = ft.ThemeMode.DARK
			self.theme_color = COLOR_PRIMARY_DARK
		else:
			self.theme_mode = ft.ThemeMode.LIGHT
			self.theme_color = COLOR_PRIMARY_LIGHT

		_ = ft.context.page.shared_preferences.get("")
		self.__saving_task = asyncio.create_task(
			pref_store(
				key=PREF_THEME_MODE,
				value=self.theme_mode.value,
			)
		)
