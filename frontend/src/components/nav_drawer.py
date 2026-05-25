from typing import Callable

import flet as ft

from components.primitives.empty import Empty
from components.styles.button_style import ButtonStyle
from constants.dimensions import DIM_DRAWER_WIDTH
from constants.spacing import SPACE_LG, SPACE_MD, SPACE_SM
from constants.styles import STYLE_RADIUS_MD


@ft.component
def NavDrawer(
	*,
	is_dismissible: bool,
	is_right: bool = False,
	is_hidden: Callable[[], bool],
	set_hidden: Callable[[bool], None],
	controls: list[ft.Control],
) -> ft.Control:

	if not is_hidden():
		return Empty()

	return ft.Row(
		controls=[
			*(is_right and [ft.VerticalDivider(width=1)] or []),
			ft.Container(
				width=DIM_DRAWER_WIDTH,
				padding=SPACE_MD,
				content=ft.Column(
					expand=True,
					spacing=SPACE_SM,
					horizontal_alignment=(
						is_right
						and ft.CrossAxisAlignment.END
						or ft.CrossAxisAlignment.START
					),
					controls=[
						*(
							is_dismissible
							and [
								ft.IconButton(
									icon=ft.Icons.MENU_OPEN,
									flip=ft.Flip(flip_x=is_right),
									tooltip="close navigation",
									on_click=lambda _: set_hidden(False),
									style=ButtonStyle()
								)
							]
							or []
						),
						*(controls),
					],
				),
			),
			*(not is_right and [ft.VerticalDivider(width=1)] or []),
		]
	)
