import platform

import flet as ft
import flet.version

from constants.images import Images, ImageSizes
from constants.phrases import Titles
from constants.typography import Fonts, FontSize
from contexts.theme import ThemeContext
from utils.app_version import get_app_version
from utils.platform import is_mobile


@ft.component
def MobileAppBar():
	theme = ft.use_context(ThemeContext)

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

	if is_mobile():
		return ft.AppBar(
			title=ft.Row(
				[
					ft.Image(
						src=Images.LOGO,
						width=ImageSizes.LOGO_SM,
						color=theme.seed_color,
					),
					ft.Text(
						Titles.APP_TITLE,
						font_family=Fonts.HEADER,
						size=FontSize.LG,
					),
				]
			),
			center_title=True,
			actions=[
				ft.IconButton(
					icon=(
						ft.Icons.DARK_MODE
						if theme.mode == ft.ThemeMode.DARK
						else ft.Icons.LIGHT_MODE
					),
					tooltip="Toggle theme",
					icon_size=ImageSizes.ICON_SM,
					on_click=lambda _: theme.toggle_mode(),
				),
				ft.PopupMenuButton(
					icon=ft.Icons.MORE_VERT,
					tooltip="Menu",
					items=[
						ft.PopupMenuItem(
							content="About",
							icon=ft.Icons.INFO_OUTLINE,
							on_click=show_about_dialog,
						)
					],
				),
			],
		)
	
	return None
