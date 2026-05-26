import asyncio
from datetime import datetime
from typing import Any, cast

import flet as ft

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_CHAT
from contexts.room import RoomContext
from models.message import Message
from repos.mock.messages import MockMessagesRepository
from repos.mock.user import MockUserRepository


@ft.component
def ChatPage():
	room_context = ft.use_context(RoomContext)

	repo, _ = ft.use_state(MockMessagesRepository())
	user_repo, _ = ft.use_state(MockUserRepository())

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_CHAT
	):
		return Empty()

	messages, set_messages = ft.use_state([])
	message_text, set_message_text = ft.use_state("")

	def load_room_data():
		async def _load():
			if room_context.room is None:
				return
			users = await user_repo.get_users()
			names = {u.id: u.name for u in users}
			raw = await repo.get_messages(room_context.room.id)
			display = [
				{
					"user": names.get(m.sender_id, m.sender_id),
					"text": m.content,
					"time": m.timestamp,
					"self": False,
				}
				for m in raw
			]
			set_messages(display)

		_ = asyncio.create_task(_load())

	ft.use_effect(
		load_room_data,
		[room_context.room.id if room_context.room else None],
	)

	def send_message(_=None):
		if not message_text.strip() or room_context.room is None:
			return

		now = datetime.now().strftime("%H:%M")
		new_id = str(int(datetime.now().timestamp() * 1000))
		msg = Message(
			id=new_id,
			room_id=room_context.room.id,
			sender_id="0",
			content=message_text.strip(),
			timestamp=now,
		)
		_ = asyncio.create_task(repo.add_message(room_context.room.id, msg))

		set_messages(
			messages
			+ [
				{
					"user": "You",
					"text": message_text.strip(),
					"time": now,
					"self": True,
				},
			]
		)
		set_message_text("")

	def on_message_change(e: ft.ControlEvent):
		event = cast(Any, e)
		set_message_text(event.data)

	def build_message(message: dict[str, Any]):
		is_self = message["self"]

		return ft.Row(
			alignment=(
				ft.MainAxisAlignment.END
				if is_self
				else ft.MainAxisAlignment.START
			),
			controls=[
				ft.Container(
					padding=12,
					border_radius=12,
					bgcolor=(
						ft.Colors.PRIMARY_CONTAINER
						if is_self
						else ft.Colors.SURFACE_CONTAINER_HIGHEST
					),
					width=400,
					content=ft.Column(
						tight=True,
						spacing=4,
						controls=[
							ft.Text(
								message["user"],
								size=12,
								weight=ft.FontWeight.BOLD,
							),
							ft.Text(
								message["text"],
								selectable=True,
							),
							ft.Text(
								message["time"],
								size=10,
								color=ft.Colors.OUTLINE,
							),
						],
					),
				),
			],
		)

	return ft.Container(
		expand=True,
		padding=16,
		content=ft.Column(
			expand=True,
			spacing=12,
			controls=[
				ft.ListView(
					expand=True,
					auto_scroll=True,
					spacing=10,
					controls=[
						build_message(message)
						for message in messages
					],
				),
				ft.Divider(height=1),
				ft.Row(
					vertical_alignment=ft.CrossAxisAlignment.END,
					controls=[
						ft.TextField(
							expand=True,
							value=message_text,
							min_lines=1,
							max_lines=5,
							hint_text="Type a message...",
							on_change=on_message_change,
							on_submit=send_message,
						),
						ft.IconButton(
							icon=ft.Icons.SEND,
							on_click=send_message,
						),
					],
				),
			],
		),
	)
