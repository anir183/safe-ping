import asyncio
import logging
from dataclasses import dataclass, field

import flet as ft

from constants.colors import Colors
from constants.storage import StorageKeys

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppModel:
	route: str

	prefs: ft.SharedPreferences = field(default_factory=ft.SharedPreferences)

	theme_mode: ft.ThemeMode = ft.ThemeMode.DARK
	theme_color: ft.Colors = Colors.DARK_SEED_COLOR

	def route_change(self, e: ft.RouteChangeEvent):
		logger.info("route changed", extra={"from": self.route, "to": e.route})
		self.route = e.route

	def navigate(self, new_route: str):
		if new_route != self.route:
			logger.info(
				"navigating routes",
				extra={"route": new_route},
			)
			_ = asyncio.create_task(ft.context.page.push_route(new_route))

	async def view_popped(self, _: ft.ViewPopEvent):
		logger.info("view popped")
		views = ft.unwrap_component(ft.context.page.views)
		if len(views) > 1:
			await ft.context.page.push_route(views[-2].route)

	async def load_theme(self):
		mode = await self.prefs.get(StorageKeys.THEME_MODE)

		logger.info(
			"loaded stored theme",
			extra={"stored": mode},
		)

		if mode == ft.ThemeMode.LIGHT.value:
			self.theme_mode = ft.ThemeMode.LIGHT
			self.theme_color = Colors.LIGHT_SEED_COLOR
		else:
			self.theme_mode = ft.ThemeMode.DARK
			self.theme_color = Colors.DARK_SEED_COLOR

	async def save_theme(self):
		_ = await self.prefs.set(
			key=StorageKeys.THEME_MODE, value=self.theme_mode.value
		)

		logger.info(
			"theme mode saved",
			extra={"mode": self.theme_mode.value},
		)

	def toggle_theme(self):
		if self.theme_mode == ft.ThemeMode.LIGHT:
			self.theme_mode = ft.ThemeMode.DARK
			self.theme_color = Colors.DARK_SEED_COLOR
		else:
			self.theme_mode = ft.ThemeMode.LIGHT
			self.theme_color = Colors.LIGHT_SEED_COLOR

		_ = asyncio.create_task(self.save_theme())
