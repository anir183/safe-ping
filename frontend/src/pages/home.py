import flet as ft

from components.navigation import Navigation
from components.room_shell import RoomShell


@ft.component
def HomePage():
	return ft.Row(
		expand=True,
		controls=[
			Navigation(),
			RoomShell(),
		],
	)
