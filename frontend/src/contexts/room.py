from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from constants.room import ROOM_SECTION_CHAT


@dataclass(frozen=True)
class RoomContextValue:
	room_id: str | None
	open_section: str
	open_room: Callable[[str | None, str | None], None]
	close_room: Callable[[], None]


RoomContext = ft.create_context(
	RoomContextValue(
		room_id=None,
		open_section=ROOM_SECTION_CHAT,
		open_room=lambda _, __: None,
		close_room=lambda: None,
	),
)
