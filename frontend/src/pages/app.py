import asyncio
import flet as ft

from components.app.room import RoomPane
from contexts.room import RoomContext, RoomContextValue
from state.room_state import RoomState


@ft.component
def AppPage() -> ft.Control:
	room_state, _ = ft.use_state(RoomState(rooms=[]))

	open_room = ft.use_callback(
		lambda id, section: room_state.open_room(id, section),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	close_room = ft.use_callback(
		lambda: room_state.close_room(),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	refresh_rooms = ft.use_callback(
		lambda: room_state.refresh_rooms(),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	room_context = ft.use_memo(
		lambda: RoomContextValue(
			room=room_state.room,
			rooms=room_state.rooms,
			open_section=room_state.open_section,
			refresh=refresh_rooms,
			open=open_room,
			close=close_room,
		),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
			open_room,
			close_room,
		],
	)

	_ = asyncio.create_task(room_context.refresh())

	room_wrapped = RoomContext(
		value=room_context,
		callback=RoomPane,
	)

	return room_wrapped
