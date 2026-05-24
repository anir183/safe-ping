import asyncio
import logging
from dataclasses import dataclass

import flet as ft

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
	route: str

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
