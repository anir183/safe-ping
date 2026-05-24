import flet as ft

from contexts.route import RouteContext


@ft.component
def RoutedPage() -> ft.Control:
	route_context = ft.use_context(RouteContext)

	match route_context.route:
		case _:
			return ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Text(route_context.route),
			)
