from typing import Callable

import flet as ft

from components.styles.button_style import ButtonStyle
from constants.dimensions import DIM_RAIL_WIDTH
from constants.spacing import SPACE_MD, SPACE_SM


@ft.component
def NavRail(
	*,
	is_right: bool = False,
	controls: list[ft.Control],
	expand: Callable[[], None] | None,
) -> ft.Control:
	return ft.Row(
		controls=[
			*(is_right and [ft.VerticalDivider(width=1)] or []),
			ft.Container(
				width=DIM_RAIL_WIDTH,
				padding=SPACE_MD,
				content=ft.Column(
					expand=True,
					spacing=SPACE_SM,
					horizontal_alignment=(ft.CrossAxisAlignment.CENTER),
					controls=[
						*(
							expand is not None
							and [
								ft.IconButton(
									icon=ft.Icons.MENU,
									tooltip="Open navigation",
									style=ButtonStyle(),
									on_click=expand,
								)
							]
							or []
						),
						*controls,
					],
				),
			),
			*(not is_right and [ft.VerticalDivider(width=1)] or []),
		]
	)
