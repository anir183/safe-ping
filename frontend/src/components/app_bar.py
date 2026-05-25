import flet as ft

from components.dialogs.info import show_info_dialog
from components.primitives.logo import Logo
from components.primitives.theme_toggle import ThemeToggle
from utils.platform import is_mobile


@ft.component
def MobileAppBar():
	if is_mobile():
		return ft.AppBar(
			title=Logo(),
			center_title=True,
			actions=[
				ThemeToggle(),
				ft.PopupMenuButton(
					icon=ft.Icons.MORE_VERT,
					tooltip="Menu",
					items=[
						ft.PopupMenuItem(
							content="About",
							icon=ft.Icons.INFO_OUTLINE,
							on_click=show_info_dialog,
						)
					],
				),
			],
		)

	return None
