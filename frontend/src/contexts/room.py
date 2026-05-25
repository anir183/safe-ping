from collections.abc import Callable
from dataclasses import dataclass
from types import CoroutineType
from typing import Any

import flet as ft

from constants.room import ROOM_SECTION_CHAT
from models.room import Room

async def noop_refresh() -> None:
	pass

@dataclass(frozen=True)
class RoomContextValue:
	room: Room | None
	rooms: list[Room]
	open_section: str
	refresh: Callable[[], CoroutineType[Any, Any, None]]
	open: Callable[[str | None, str | None], None]
	close: Callable[[], None]


RoomContext = ft.create_context(
	RoomContextValue(
		room=None,
		rooms=[],
		open_section=ROOM_SECTION_CHAT,
		refresh=noop_refresh,
		open=lambda _, __: None,
		close=lambda: None,
	),
)
