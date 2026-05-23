import flet as ft

from pages.home import HomePage


def get_page_for_route(route: str) -> ft.Control:
	match route:
		case "/":
			return HomePage()

		case "/login":
			return ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Text("Login Page"),
			)

		case _:
			return ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Text("404 - Page Not Found"),
			)
