import flet as ft

from components.app.room_nav import RoomNav
from contexts.room import RoomContext


@ft.component
def RoomPane():
	room_context = ft.use_context(RoomContext)
	return ft.Row(
		expand=True,
		controls=[
			RoomNav(),
			ft.Container(
				expand=True,
				alignment=ft.Alignment.CENTER,
				content=ft.Text(
					room_context.room and room_context.room.name or "Dashboard"
				),
			),
		],
	)
