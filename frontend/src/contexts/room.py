from dataclasses import dataclass
from collections.abc import Callable
import flet as ft

from constants.room import RoomSection


@dataclass(frozen=True)
class RoomContextValue:
	room_id: str | None
	active_section: RoomSection

	set_room_id: Callable[[str | None], None]
	set_section: Callable[[RoomSection], None]

	open_room: Callable[[str], None]
	close_room: Callable[[], None]


RoomContext = ft.create_context(
	RoomContextValue(
		room_id=None,
		active_section=RoomSection.CHAT,

		set_room_id=lambda _: None,
		set_section=lambda _: None,

		open_room=lambda _: None,
		close_room=lambda: None,
	)
)
