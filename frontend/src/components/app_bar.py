import platform

import flet as ft
import flet.version

from constants.dimensions import Dimensions
from constants.images import Images, ImageSizes
from constants.phrases import Titles
from constants.spacing import Spacing
from constants.typography import Fonts, FontSize
from contexts.theme import ThemeContext
from utils.app_version import get_app_version
from utils.platform import platform_view


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

	def minimize(_):
		ft.context.page.window.minimized = True
		ft.context.page.update()

	def toggle_maximize(_):
		page = ft.context.page
		page.window.maximized = not bool(page.window.maximized)
		page.update()

	async def close(_):
		await ft.context.page.window.close()

	return platform_view(
		desktop=lambda: ft.WindowDragArea(
			content=ft.Container(
				height=Dimensions.APP_BAR_HEIGHT,
				padding=ft.Padding.symmetric(horizontal=Spacing.MD),
				content=ft.Row(
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					controls=[
						ft.Row(
							spacing=Spacing.MD,
							vertical_alignment=ft.CrossAxisAlignment.CENTER,
							controls=[
								ft.Image(
									src=Images.LOGO,
									width=ImageSizes.LOGO_SM,
									color=ft.use_context(
										ThemeContext
									).seed_color,
								),
								ft.Text(
									Titles.APP_TITLE,
									font_family=Fonts.HEADER,
									size=FontSize.LG,
								),
							],
						),
						ft.Row(
							spacing=Spacing.NONE,
							controls=[
								ft.IconButton(
									icon=ft.Icons.INFO_OUTLINE,
									tooltip="About",
									icon_size=ImageSizes.ICON_SM,
									on_click=show_about_dialog,
								),
								ft.IconButton(
									icon=ft.Icons.MINIMIZE,
									tooltip="Minimize",
									icon_size=ImageSizes.ICON_SM,
									on_click=minimize,
								),
								ft.IconButton(
									icon=ft.Icons.CROP_SQUARE,
									tooltip="Maximize",
									icon_size=ImageSizes.ICON_SM,
									on_click=toggle_maximize,
								),
								ft.IconButton(
									icon=ft.Icons.CLOSE,
									tooltip="Close",
									icon_size=ImageSizes.ICON_SM,
									on_click=close,
								),
							],
						),
					],
				),
			)
		),
		mobile=lambda: ft.AppBar(
			title=ft.Row(
				[
					ft.Image(
						src=Images.LOGO,
						width=ImageSizes.LOGO_SM,
						color=ft.use_context(ThemeContext).seed_color,
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
		),
		web=lambda: ft.WindowDragArea(
			content=ft.Container(
				height=Dimensions.APP_BAR_HEIGHT,
				padding=ft.Padding.symmetric(horizontal=Spacing.MD),
				content=ft.Row(
					[
						ft.Image(
							src=Images.LOGO,
							width=ImageSizes.LOGO_SM,
							color=ft.use_context(ThemeContext).seed_color,
						),
						ft.Text(
							Titles.APP_TITLE,
							font_family=Fonts.HEADER,
							size=FontSize.LG,
						),
					],
				),
			)
		),
	)
