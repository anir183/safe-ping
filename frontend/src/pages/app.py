import flet as ft

from components.app.room_nav import RoomNav
from contexts.room import RoomContext, RoomContextValue
from state.room_state import RoomState


@ft.component
def AppPage() -> ft.Control:
	room_state, _ = ft.use_state(RoomState(room_id=None))

	open_room = ft.use_callback(
		lambda id, section: room_state.open_room(id, section),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
		],
	)

	close_room = ft.use_callback(
		lambda: room_state.close_room(),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
		],
	)

	room_context = ft.use_memo(
		lambda: RoomContextValue(
			room_id=room_state.room_id,
			open_section=room_state.open_section,
			open_room=open_room,
			close_room=close_room,
		),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
			open_room,
			close_room,
		],
	)

	room_wrapped = RoomContext(
		value=room_context,
		callback=lambda: ft.Row(
			expand=True,
			controls=[
				RoomNav(),
				ft.Container(
					expand=True,
					alignment=ft.Alignment.CENTER,
					content=ft.Text(room_context.room_id or "Dashboard"),
				),
			],
		),
	)

	return room_wrapped
