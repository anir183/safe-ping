import flet as ft

from components.navigation import Navigation
from components.room_shell import RoomShell
from constants.navigation import NavID
from contexts.navigation import (
	NavigationContext,
	NavigationContextValue,
)


@ft.component
def HomePage():
	selected, set_selected = ft.use_state(NavID.DASH)

	return NavigationContext(
		NavigationContextValue(
			selected=selected,
			set_selected=set_selected,
		),
		lambda: ft.Row(
			expand=True,
			controls=[
				Navigation(),
				RoomShell(selected),
			],
		),
	)
