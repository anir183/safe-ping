import asyncio
import logging
from dataclasses import dataclass

import flet as ft

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppModel:
	route: str
	theme_mode: ft.ThemeMode = ft.ThemeMode.DARK
	theme_color: ft.Colors = ft.Colors.LIME

	def route_change(self, e: ft.RouteChangeEvent):
		logger.info("route changed", extra={"from": self.route, "to": e.route})
		self.route = e.route

	def navigate(self, new_route: str):
		if new_route != self.route:
			logger.info("navigating to:", new_route)
			_ = asyncio.create_task(ft.context.page.push_route(new_route))

	async def view_popped(self, _: ft.ViewPopEvent):
		logger.info("view popped")
		views = ft.unwrap_component(ft.context.page.views)
		if len(views) > 1:
			await ft.context.page.push_route(views[-2].route)

	def toggle_theme(self):
		self.theme_mode = (
			ft.ThemeMode.DARK
			if self.theme_mode == ft.ThemeMode.LIGHT
			else ft.ThemeMode.LIGHT
		)

	def set_theme_color(self, color: ft.Colors):
		self.theme_color = color
