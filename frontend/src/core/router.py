import flet as ft

from constants.routes import ROUTE_APP, ROUTE_ROOT
from pages.app import AppPage
from pages.landing import LandingPage
from pages.not_found import NotFound


@ft.component
def Router() -> ft.Control:
	return ft.Router(
		routes=[
			ft.Route(
				path=ROUTE_ROOT,
				index=True,
				component=LandingPage,
			),
			ft.Route(
				path=ROUTE_APP,
				component=AppPage,
			),
		],
		not_found=NotFound,
	)
