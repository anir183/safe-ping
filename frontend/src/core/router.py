import flet as ft

from constants.routes import ROUTE_HOME, ROUTE_ROOT
from pages.home import HomePage
from pages.not_found import NotFound


@ft.component
def Router() -> ft.Control:
	return ft.Router(
		routes=[
			ft.Route(path=ROUTE_ROOT, index=True, component=HomePage),
			ft.Route(path=ROUTE_HOME, index=True, component=HomePage),
		],
		not_found=NotFound,
	)
