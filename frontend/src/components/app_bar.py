import platform

import flet as ft
import flet.version

from constants.images import ImageSizes, Images
from constants.phrases import Titles
from utils.app_version import get_app_version


@ft.component
def AppBar():
	def show_about_dialog():
		ft.context.page.show_dialog(
			ft.AlertDialog(
				title=ft.Text("About " + Titles.APP_TITLE),
				content=ft.Column(
					tight=True,
					controls=[
						ft.Text(
							f"{Titles.APP_TITLE} version: {get_app_version()}"
						),
						ft.Text(f"Flet version: {flet.version.flet_version}"),
						ft.Text(
							f"Flutter version: {flet.version.flutter_version}"
						),
						ft.Text(f"Python version: {platform.python_version()}"),
					],
				),
				actions=[
					ft.TextButton(
						"Close", on_click=lambda _: ft.context.page.pop_dialog()
					)
				],
			)
		)

	return ft.AppBar(
		title=ft.Row(
			[
				ft.Image(src=Images.LOGO, width=ImageSizes.LOGO_SM),
				ft.Text(Titles.APP_TITLE),
			]
		),
		center_title=True,
		actions=[
			ft.PopupMenuButton(
				icon=ft.Icons.MORE_VERT,
				tooltip="Menu",
				items=[
					ft.PopupMenuItem(
						content="About",
						on_click=show_about_dialog,
					)
				],
			),
		],
	)
