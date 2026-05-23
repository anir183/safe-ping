import flet as ft

from components.navigation import Navigation
from constants.navigation import NavID
from constants.typography import FontSize
from contexts.navigation import (
	NavigationContext,
	NavigationContextValue,
)


@ft.component
def HomePage():
	selected, set_selected = ft.use_state(NavID.DASH)

	def content() -> ft.Control:
		match selected:
			case NavID.CHAT_1:
				text = "Chat 1 Area"

			case NavID.CHAT_2:
				text = "Chat 2 Area"

			case NavID.CHAT_3:
				text = "Chat 3 Area"

			case _:
				text = "Dashboard Area"

		return ft.Container(
			expand=True,
			alignment=ft.Alignment.CENTER,
			content=ft.Text(
				text,
				size=FontSize.XL,
			),
		)

	return NavigationContext(
		NavigationContextValue(
			selected=selected,
			set_selected=set_selected,
		),
		lambda: ft.Row(
			expand=True,
			controls=[
				Navigation(),
				content(),
			],
		),
	)
