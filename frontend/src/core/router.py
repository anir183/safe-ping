import flet as ft

from contexts.route import RouteContext
from contexts.theme import ThemeContext


@ft.component
def RoutedPage() -> ft.Control:
	route_context = ft.use_context(RouteContext)
	theme_context = ft.use_context(ThemeContext)

	match route_context.route:
		case _:
			return ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Button(
					route_context.route,
					on_click=theme_context.toggle_mode,
				),
			)
