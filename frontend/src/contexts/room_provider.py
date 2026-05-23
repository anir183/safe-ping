import flet as ft
from collections.abc import Callable

from constants.room import RoomSection
from contexts.room import RoomContext, RoomContextValue


@ft.component
def RoomProvider(children: Callable[[], ft.Control]):
	room_id: str | None
	set_room_id: Callable
	room_id, set_room_id = ft.use_state(None)
	section, set_section = ft.use_state(RoomSection.CHAT)

	def open_room(new_id: str):
		set_room_id(new_id)
		set_section(RoomSection.CHAT)  # reset view on room switch

	def close_room():
		set_room_id(None)
		set_section(RoomSection.CHAT)

	value = ft.use_memo(
		lambda: RoomContextValue(
			room_id=room_id,
			active_section=section,

			set_room_id=set_room_id,
			set_section=set_section,

			open_room=open_room,
			close_room=close_room,
		),
		dependencies=[room_id, section],
	)

	return RoomContext(value, lambda: children())
