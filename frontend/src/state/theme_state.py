import asyncio
import logging
from dataclasses import dataclass, field

import flet as ft

from constants.colors import (
	COLOR_ALT_DARK,
	COLOR_ALT_LIGHT,
	COLOR_PRIMARY_DARK,
	COLOR_PRIMARY_LIGHT,
)
from constants.fonts import FONT_BODY
from constants.prefs import PREF_THEME_MODE
from services.shared_prefs import pref_retrieve, pref_store

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class ThemeState:
	route: str

	theme_mode: ft.ThemeMode = ft.ThemeMode.DARK
	theme_primary: ft.Theme = field(
		default_factory=lambda: ft.Theme(
			color_scheme_seed=COLOR_PRIMARY_DARK,
			font_family=FONT_BODY,
		)
	)
	theme_secondary: ft.Theme = field(
		default_factory=lambda: ft.Theme(
			color_scheme_seed=COLOR_ALT_DARK,
			font_family=FONT_BODY,
		)
	)

	width: ft.Number = 0
	height: ft.Number = 0

	def on_resize(self):
		self.width = ft.context.page.width or 0
		self.height = ft.context.page.height or 0

		logger.info(
			"resized window",
			extra={
				"width": self.width,
				"height": self.height,
			},
		)

	def __generate_themes(self):
		if self.theme_mode == ft.ThemeMode.DARK:
			color = COLOR_PRIMARY_DARK
			color_alt = COLOR_ALT_DARK
		else:
			color = COLOR_PRIMARY_LIGHT
			color_alt = COLOR_ALT_LIGHT

		self.theme_primary = ft.Theme(
			color_scheme_seed=color,
			font_family=FONT_BODY,
		)
		self.theme_secondary = ft.Theme(
			color_scheme_seed=color_alt,
			font_family=FONT_BODY,
		)

	async def load_theme(self):
		mode = await pref_retrieve(PREF_THEME_MODE)

		logger.info(
			"loaded stored theme",
			extra={"stored": mode},
		)

		if mode == ft.ThemeMode.LIGHT.value:
			self.theme_mode = ft.ThemeMode.LIGHT
		else:
			self.theme_mode = ft.ThemeMode.DARK
		self.__generate_themes()

	__saving_task = None

	def toggle_theme(self):
		if self.__saving_task and not self.__saving_task.done():
			return

		if self.theme_mode == ft.ThemeMode.LIGHT:
			self.theme_mode = ft.ThemeMode.DARK
		else:
			self.theme_mode = ft.ThemeMode.LIGHT
		self.__generate_themes()

		_ = ft.context.page.shared_preferences.get("")
		self.__saving_task = asyncio.create_task(
			pref_store(
				key=PREF_THEME_MODE,
				value=self.theme_mode.value,
			)
		)
