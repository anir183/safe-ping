import asyncio

import flet as ft

from components.app.room_list import RoomList
from components.nav_drawer import NavDrawer
from components.nav_rail import NavRail
from repos.mock.room import MockRoomRepository
from utils.responsive import is_extra_large, is_large, is_medium, is_small


@ft.component
def RoomNav():
	drawer_expanded, set_drawer_expanded = ft.use_state(
		is_large() or is_extra_large()
	)

	rooms, set_rooms = ft.use_state([])

	repo = MockRoomRepository()

	async def list_rooms():
		set_rooms(await repo.get_rooms())

	ft.use_effect(lambda: asyncio.create_task(list_rooms()), [])

	drawer = NavDrawer(
		is_dismissible=is_small() or is_medium(),
		is_hidden=lambda: drawer_expanded,
		set_hidden=set_drawer_expanded,
		controls=[
			RoomList(
				rooms=rooms,
				compact=False,
			)
		],
	)

	rail = NavRail(
		expand=lambda: set_drawer_expanded(True),
		controls=[
			RoomList(
				rooms=rooms,
				compact=True,
			)
		],
	)

	return drawer if drawer_expanded else rail
