import flet as ft

from components.platform import PlatformComponent
from components.responsive import ResponsiveComponent


@ft.component
def HomePage() -> ft.Control:
	return ft.Container(
		expand=True,
		alignment=ft.Alignment.CENTER,
		content=ft.Column(
			expand=True,
			alignment=ft.MainAxisAlignment.CENTER,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Text(f"{ft.context.page.width} x {ft.context.page.height}"),
				PlatformComponent(
					desktop=lambda: ft.Text("Desktop"),
					mobile=lambda: ft.Text("Mobile"),
					web=lambda: ft.Text("Web"),
					fallback=lambda: ft.Text("Fallback"),
				),
				ResponsiveComponent(
					small=lambda: ft.Text("Small"),
					medium=lambda: ft.Text("Medium"),
					large=lambda: ft.Text("Large"),
					extra_large=lambda: ft.Text("XLarge"),
					fallback=lambda: ft.Text("Fallback"),
				),
			],
		),
	)
