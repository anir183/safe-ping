import asyncio
from datetime import datetime
from typing import Any, cast

import flet as ft

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_CHAT
from contexts.room import RoomContext
from contexts.user import UserContext
from models.message import Message
from repos.mock.messages import MockMessagesRepository
from repos.mock.user import MockUserRepository
from services.ws import WsConnection
from utils.crypto import decrypt as crypto_decrypt
from utils.crypto import encrypt as crypto_encrypt


def _try_decrypt(content: str) -> str:
	try:
		return crypto_decrypt(content)
	except Exception:
		return content


@ft.component
def ChatPage():
	room_context = ft.use_context(RoomContext)
	user_context = ft.use_context(UserContext)

	repo, _ = ft.use_state(MockMessagesRepository())
	user_repo, _ = ft.use_state(MockUserRepository())

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_CHAT
	):
		return Empty()

	messages, set_messages = ft.use_state([])
	message_text, set_message_text = ft.use_state("")
	ws_state, set_ws_state = ft.use_state(
		{"conn": None, "active": False, "id": 0}
	)

	current_user = user_context.user
	current_id = current_user.id if current_user else None

	def _decrypt_display(m: dict) -> dict:
		return {
			"user": m.get("sender_name", m.get("sender_id", "Unknown")),
			"text": _try_decrypt(m.get("content", "")),
			"time": m.get("timestamp", ""),
			"self": m.get("sender_id") == current_id,
		}

	def _handle_ws_init(history: list[dict]) -> None:
		if history:
			display = [_decrypt_display(m) for m in history]
			set_messages(display)
		else:
			_ = asyncio.create_task(_load_from_mock())

		set_ws_state(
			lambda prev: {**prev, "active": True, "id": len(history)}
		)

	def _handle_ws_message(msg_data: dict) -> None:
		display = _decrypt_display(msg_data)

		def append_messages(prev: list) -> list:
			out = list(prev)
			out.append(display)
			return out

		set_messages(append_messages)

	async def _load_from_mock() -> None:
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
				"self": m.sender_id == current_id,
			}
			for m in raw
		]
		set_messages(display)

	def _member_of(room: Any) -> bool:
		if current_id is None:
			return False
		return current_id == room.owner_id or current_id in room.member_ids

	def setup_room():
		async def _setup():
			old_state = ws_state
			if old_state["conn"]:
				await old_state["conn"].disconnect()

			if room_context.room is None:
				return

			conn = WsConnection()
			ok = await conn.connect(
				room_id=room_context.room.id,
				user_id=current_id or "0",
				on_init=_handle_ws_init,
				on_message=_handle_ws_message,
			)

			if ok:
				set_ws_state(
					{"conn": conn, "active": True, "id": 0}
				)
			else:
				set_ws_state(
					{"conn": None, "active": False, "id": 0}
				)
				await _load_from_mock()

		_ = asyncio.create_task(_setup())

	ft.use_effect(
		setup_room,
		[room_context.room.id if room_context.room else None],
	)

	def send_message(_=None):
		if (
			not message_text.strip()
			or room_context.room is None
		):
			return

		if not _member_of(room_context.room):
			return

		now = datetime.now().strftime("%H:%M")
		new_id = ws_state["id"] + 1
		set_ws_state({**ws_state, "id": new_id})

		sender_id = current_id or "0"
		sender_name = current_user.name if current_user else "You"
		raw_content = message_text.strip()
		encrypted = crypto_encrypt(raw_content) if ws_state["active"] else raw_content

		data = {
			"type": "message",
			"id": str(new_id),
			"room_id": room_context.room.id,
			"sender_id": sender_id,
			"sender_name": sender_name,
			"content": encrypted,
			"timestamp": now,
		}

		display = {
			"user": sender_name,
			"text": raw_content,
			"time": data["timestamp"],
			"self": True,
		}

		if ws_state["active"] and ws_state["conn"]:
			_ = asyncio.create_task(ws_state["conn"].send(data))
		else:
			msg = Message(
				id=str(new_id),
				room_id=room_context.room.id,
				sender_id=sender_id,
				content=raw_content,
				timestamp=now,
			)
			_ = asyncio.create_task(
				repo.add_message(room_context.room.id, msg)
			)

		set_messages(messages + [display])
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

	backend_status = (
		"Connected"
		if ws_state["active"]
		else "Offline"
	)

	return ft.Container(
		expand=True,
		padding=16,
		content=ft.Column(
			expand=True,
			spacing=12,
			controls=[
				ft.Row(
					alignment=ft.MainAxisAlignment.END,
					controls=[
						ft.Container(
							padding=ft.Padding.symmetric(
								horizontal=8, vertical=4
							),
							border_radius=12,
							bgcolor=(
								ft.Colors.GREEN_100
								if ws_state["active"]
								else ft.Colors.GREY_300
							),
							content=ft.Text(
								backend_status,
								size=10,
								color=ft.Colors.BLACK,
							),
						),
					],
				),
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
