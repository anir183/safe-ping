import logging
from dataclasses import dataclass

import flet as ft

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class AppState:
	route: str

	def route_change(self, e: ft.RouteChangeEvent) -> None:
		logger.info(
			"route changed",
			extra={
				"from": self.route,
				"to": e.route,
			},
		)
		self.route = e.route
