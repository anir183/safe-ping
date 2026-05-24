import flet as ft


def routed_page(route: str = "test") -> ft.Control:
	match route:
		case _:
			return ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Text(route),
			)
