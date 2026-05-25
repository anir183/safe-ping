import flet as ft

from components.primitives.empty import Empty
from contexts.room import RoomContext


@ft.component
def Dashboard():
	room_context = ft.use_context(RoomContext)

	if room_context.room is not None:
		return Empty()

	return ft.Container(
		expand=True,
		content=ft.Column(
			expand=True,
			alignment=ft.MainAxisAlignment.CENTER,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Text(
					"Dashboard",
					align=ft.Alignment.CENTER,
				),
			],
		),
	)
