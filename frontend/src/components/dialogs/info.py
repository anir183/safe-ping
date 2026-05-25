import platform

import flet as ft
import flet.version

from components.util.responsive import ResponsiveComponent
from constants.fonts import FONT_MONO
from constants.info import APP_AUTHORS, APP_TITLE, APP_VERSION
from constants.spacing import SPACE_SM


def show_info_dialog():
	page = ft.context.page
	page.show_dialog(
		ft.AlertDialog(
			title=ft.Text("Info @ " + APP_TITLE),
			content=ft.Column(
				tight=True,
				spacing=SPACE_SM,
				controls=[
					ft.Text(f"{APP_TITLE} commit: {APP_VERSION}"),
					ft.Text(f"Flet version: {flet.version.flet_version}"),
					ft.Text(f"Flutter version: {flet.version.flutter_version}"),
					ft.Text(f"Python version: {platform.python_version()}"),
					ResponsiveComponent(
						small=lambda: ft.Text(
							f"\n{APP_AUTHORS}",
							font_family=FONT_MONO,
						),
						fallback=lambda: ft.Row(
							[
								ft.Text(
									f"\n{APP_AUTHORS}",
									font_family=FONT_MONO,
								),
								ft.Container(width=SPACE_SM),
							],
						),
					),
				],
			),
			actions=[
				ft.TextButton("Close", on_click=lambda _: page.pop_dialog())
			],
		)
	)
