import flet as ft

from components.dialogs.info import show_info_dialog
from components.platform import PlatformComponent
from components.primitives.logo import Logo
from components.primitives.theme_toggle import ThemeToggle
from constants.dimensions import DIM_APP_HEADER_HEIGHT
from constants.images import ICON_SM
from constants.spacing import SPACE_MD, SPACE_NONE


@ft.component
def AppHeader() -> ft.Control:
	def minimize(_):
		ft.context.page.window.minimized = True
		ft.context.page.update()

	def toggle_maximize(_):
		page = ft.context.page
		page.window.maximized = not bool(page.window.maximized)
		page.update()

	async def close(_):
		await ft.context.page.window.close()

	return PlatformComponent(
		desktop=lambda: ft.WindowDragArea(
			content=ft.Container(
				height=DIM_APP_HEADER_HEIGHT,
				padding=ft.Padding.symmetric(horizontal=SPACE_MD),
				content=ft.Row(
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					vertical_alignment=ft.CrossAxisAlignment.CENTER,
					controls=[
						Logo(),
						ft.Row(
							spacing=SPACE_NONE,
							controls=[
								ThemeToggle(),
								ft.IconButton(
									icon=ft.Icons.INFO_OUTLINE,
									tooltip="info",
									icon_size=ICON_SM,
									on_click=show_info_dialog,
								),
								ft.IconButton(
									icon=ft.Icons.MINIMIZE,
									tooltip="minimize",
									icon_size=ICON_SM,
									on_click=minimize,
								),
								ft.IconButton(
									icon=ft.Icons.CROP_SQUARE,
									tooltip="maximize",
									icon_size=ICON_SM,
									on_click=toggle_maximize,
								),
								ft.IconButton(
									icon=ft.Icons.CLOSE,
									tooltip="close",
									icon_size=ICON_SM,
									on_click=close,
								),
							],
						),
					],
				),
			)
		),
		web=lambda: ft.Container(
			height=DIM_APP_HEADER_HEIGHT,
			padding=ft.Padding.symmetric(horizontal=SPACE_MD),
			content=ft.Row(
				alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
				vertical_alignment=ft.CrossAxisAlignment.CENTER,
				controls=[
					Logo(),
					ft.Row(
						spacing=SPACE_NONE,
						controls=[
							ThemeToggle(),
							ft.IconButton(
								icon=ft.Icons.INFO_OUTLINE,
								tooltip="info",
								icon_size=ICON_SM,
								on_click=show_info_dialog,
							),
						],
					),
				],
			),
		),
	)
