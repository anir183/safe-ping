import platform

import flet as ft
import flet.version

from constants.info import APP_AUTHORS, APP_TITLE, APP_VERSION
from constants.spacing import SPACE_SM


def show_info_dialog():
	ft.context.page.show_dialog(
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
					ft.Text(f"\n{APP_AUTHORS}", font_family="Monospace"),
				],
			),
			actions=[
				ft.TextButton(
					"Close", on_click=lambda _: ft.context.page.pop_dialog()
				)
			],
		)
	)
