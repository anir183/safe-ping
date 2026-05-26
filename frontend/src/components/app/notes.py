import asyncio
from datetime import datetime
from typing import Any, cast

import flet as ft

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_NOTES
from contexts.room import RoomContext
from models.notes import Note
from repos.mock.notes import MockNotesRepository


@ft.component
def NotesPage():
	room_context = ft.use_context(RoomContext)

	repo, _ = ft.use_state(MockNotesRepository())

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_NOTES
	):
		return Empty()

	title, set_title = ft.use_state("")
	content, set_content = ft.use_state("")
	saved_at, set_saved_at = ft.use_state("Not saved")

	def load_note():
		async def _load():
			if room_context.room is None:
				return
			note = await repo.get_note(room_context.room.id)
			if note is not None:
				set_title(note.title)
				set_content(note.content)
				set_saved_at(note.updated_at)
			else:
				set_title("")
				set_content("")
				set_saved_at("Not saved")

		_ = asyncio.create_task(_load())

	ft.use_effect(
		load_note,
		[room_context.room.id if room_context.room else None],
	)

	def save_note(_=None):
		if room_context.room is None:
			return

		now = datetime.now().strftime("%a %H:%M:%S")
		note = Note(
			id=room_context.room.id,
			room_id=room_context.room.id,
			title=title,
			content=content,
			created_at=now,
			updated_at=now,
		)
		_ = asyncio.create_task(repo.save_note(room_context.room.id, note))
		set_saved_at(f"Saved at {now}")

	def on_title_change(e: ft.ControlEvent):
		event = cast(Any, e)
		set_title(event.data)

	def on_content_change(e: ft.ControlEvent):
		event = cast(Any, e)
		set_content(event.data)

	return ft.Container(
		expand=True,
		padding=16,
		content=ft.Column(
			expand=True,
			spacing=16,
			controls=[
				ft.Row(
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					controls=[
						ft.Text(
							saved_at,
							size=12,
							color=ft.Colors.OUTLINE,
						),
						ft.FilledButton(
							"Save",
							icon=ft.Icons.SAVE,
							on_click=save_note,
						),
					],
				),
				ft.Divider(),
				ft.TextField(
					value=title,
					text_size=24,
					border=ft.InputBorder.NONE,
					hint_text="Untitled Note",
					on_change=on_title_change,
				),
				ft.Container(
					expand=True,
					border_radius=12,
					bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
					padding=12,
					content=ft.TextField(
						expand=True,
						value=content,
						multiline=True,
						min_lines=20,
						max_lines=None,
						border=ft.InputBorder.NONE,
						hint_text="Start writing...",
						on_change=on_content_change,
					),
				),
			],
		),
	)
