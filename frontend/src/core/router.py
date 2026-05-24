import flet as ft

from pages.not_found import NotFound


@ft.component
def Router() -> ft.Control:
	return ft.Router(
		routes=[
			ft.Route(index=True, component=ft.Placeholder)
		],
		not_found=NotFound,
	)
