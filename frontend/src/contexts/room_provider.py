from collections.abc import Callable

import flet as ft

from constants.room import RoomSection
from contexts.room import RoomContext, RoomContextValue


@ft.component
def RoomProvider(children: Callable[[], ft.Control]) -> ft.Control:
	section, set_section = ft.use_state(RoomSection.CHAT)

	active_chat_id: str | None
	set_chat_id: Callable
	active_whiteboard_id: str | None
	set_whiteboard_id: Callable
	active_note_id: str | None
	set_note_id: Callable

	active_chat_id, set_chat_id = ft.use_state(None)
	active_whiteboard_id, set_whiteboard_id = ft.use_state(None)
	active_note_id, set_note_id = ft.use_state(None)

	def open_chat(chat_id: str):
		set_section(RoomSection.CHAT)
		set_chat_id(chat_id)

	def open_whiteboard(wb_id: str):
		set_section(RoomSection.WHITEBOARD)
		set_whiteboard_id(wb_id)

	def open_note(note_id: str):
		set_section(RoomSection.NOTES)
		set_note_id(note_id)

	def set_section_action(sec: RoomSection):
		set_section(sec)

	def close_panel():
		set_chat_id(None)
		set_whiteboard_id(None)
		set_note_id(None)

	value = ft.use_memo(
		lambda: RoomContextValue(
			active_section=section,

			active_chat_id=active_chat_id,
			active_whiteboard_id=active_whiteboard_id,
			active_note_id=active_note_id,

			set_section=set_section_action,
			open_chat=open_chat,
			open_whiteboard=open_whiteboard,
			open_note=open_note,
			close_panel=close_panel,
		),
		dependencies=[
			section,
			active_chat_id,
			active_whiteboard_id,
			active_note_id,
		],
	)

	return RoomContext(value, lambda: children())
