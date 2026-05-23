from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from constants.room import RoomSection


@dataclass(frozen=True)
class RoomContextValue:
	active_section: RoomSection

	active_chat_id: str | None
	active_whiteboard_id: str | None
	active_note_id: str | None

	set_section: Callable[[RoomSection], None]

	open_chat: Callable[[str], None]
	open_whiteboard: Callable[[str], None]
	open_note: Callable[[str], None]

	close_panel: Callable[[], None]


RoomContext = ft.create_context(
	RoomContextValue(
		active_section=RoomSection.CHAT,
		active_chat_id=None,
		active_whiteboard_id=None,
		active_note_id=None,

		set_section=lambda _: None,

		open_chat=lambda _: None,
		open_whiteboard=lambda _: None,
		open_note=lambda _: None,

		close_panel=lambda: None,
	)
)
