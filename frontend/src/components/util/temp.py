import flet as ft

from components.dialogs.info import show_info_dialog
from components.util.platform import PlatformComponent
from components.util.responsive import ResponsiveComponent
from constants.routes import ROUTE_APP
from constants.spacing import SPACE_MD
from contexts.theme import ThemeContext


@ft.component
def Temp() -> ft.Control:
	theme_context = ft.use_context(ThemeContext)

	return ft.Container(
		expand=True,
		alignment=ft.Alignment.CENTER,
		content=ft.Column(
			expand=True,
			alignment=ft.MainAxisAlignment.CENTER,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			spacing=SPACE_MD,
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
				ft.Button(
					"app",
					on_click=lambda: ft.context.page.navigate(ROUTE_APP),
				),
				ft.Button(
					f"{theme_context.mode.value}",
					on_click=theme_context.toggle_mode,
				),
				ft.Button(
					"info",
					on_click=show_info_dialog,
				),
			],
		),
	)
