# import flet as ft
#
# from components.primitives.empty import Empty
# from constants.room import ROOM_SECTION_NOTES
# from contexts.room import RoomContext
#
#
# @ft.component
# def NotesPage():
# 	room_context = ft.use_context(RoomContext)
#
# 	if (
# 		room_context.room is None
# 		or room_context.open_section != ROOM_SECTION_NOTES
# 	):
# 		return Empty()
#
# 	return ft.Container(
# 		expand=True,
# 		content=ft.Column(
# 			expand=True,
# 			alignment=ft.MainAxisAlignment.CENTER,
# 			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# 			controls=[
# 				ft.Text(
# 					room_context.room and room_context.room.name,
# 					align=ft.Alignment.CENTER,
# 				),
# 				ft.Text(
# 					room_context.open_section,
# 					align=ft.Alignment.CENTER,
# 				),
# 			],
# 		),
# 	)

from datetime import datetime
from typing import Any, cast

import flet as ft

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_NOTES
from contexts.room import RoomContext


@ft.component
def NotesPage():
	room_context = ft.use_context(RoomContext)

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_NOTES
	):
		return Empty()

	title, set_title = ft.use_state("")
	content, set_content = ft.use_state("")
	saved_at, set_saved_at = ft.use_state("Not saved")

	def save_note(_=None):
		set_saved_at(f"Saved at {datetime.now().strftime('%H:%M:%S')}")

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
