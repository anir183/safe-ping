import asyncio
from typing import Callable

import flet as ft

from components.styles.button_style import ButtonStyle
from constants.room import ROOM_SECTION_CHAT
from constants.spacing import SPACE_SM
from contexts.room import RoomContext
from repos.rooms import RoomsRepository


@ft.component
def RoomsList(repo: RoomsRepository):
	rooms: list[ft.Control]
	set_rooms: Callable[[list[ft.Control]], None]
	rooms, set_rooms = ft.use_state(
		[
			ft.TextButton(
				width=float("inf"),
				icon=ft.Icons.DOWNLOADING,
				content="Loading...",
				style=ButtonStyle(),
			)
		]
	)

	room_context = ft.use_context(RoomContext)

	def switch_room(name: str):
		room_context.open_room(
			name,
			ROOM_SECTION_CHAT,
		)

	async def list_rooms():
		global rooms

		got_rooms = await repo.get_rooms()
		set_rooms(
			[
				ft.TextButton(
					width=float("inf"),
					icon=ft.Icons.CHAT,
					content=room.name,
					on_click=lambda _, room_name=room.name: switch_room(
						room_name
					),
					style=ButtonStyle(),
				)
				for room in got_rooms
			]
		)

	def fetch_rooms():
		_ = asyncio.create_task(list_rooms())

	ft.use_effect(fetch_rooms, [])

	return ft.ListView(
		expand=True,
		spacing=SPACE_SM,
		controls=rooms,
	)
