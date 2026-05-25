import flet as ft

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_CHAT
from contexts.room import RoomContext


@ft.component
def ChatPage():
	room_context = ft.use_context(RoomContext)

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_CHAT
	):
		return Empty()

	return ft.Container(
		expand=True,
		content=ft.Column(
			expand=True,
			alignment=ft.MainAxisAlignment.CENTER,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Text(
					room_context.room and room_context.room.name,
					align=ft.Alignment.CENTER,
				),
				ft.Text(
					room_context.open_section,
					align=ft.Alignment.CENTER,
				),
			],
		),
	)
