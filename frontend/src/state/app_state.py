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

	def push_route(self, new_route: str):
		if new_route != self.route:
			logger.info(
				"navigating routes",
				extra={
					"route": new_route,
				},
			)
			_ = asyncio.create_task(
				ft.context.page.push_route(new_route),
			)

	def on_route_change(self, e: ft.RouteChangeEvent) -> None:
		logger.info(
			"route changed",
			extra={
				"from": self.route,
				"to": e.route,
			},
		)
		self.route = e.route

	async def on_view_pop(self, _: ft.ViewPopEvent):
		logger.info("view popped")
		views = ft.unwrap_component(ft.context.page.views)
		if len(views) > 1:
			await ft.context.page.push_route(views[-2].route)

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

	def toggle_theme(self):
		if self.theme_mode == ft.ThemeMode.LIGHT:
			self.theme_mode = ft.ThemeMode.DARK
			self.theme_color = COLOR_PRIMARY_DARK
		else:
			self.theme_mode = ft.ThemeMode.LIGHT
			self.theme_color = COLOR_PRIMARY_LIGHT

		_ = asyncio.create_task(
			pref_store(
				key=PREF_THEME_MODE,
				value=self.theme_mode.value,
			)
		)
