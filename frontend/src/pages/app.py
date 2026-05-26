import asyncio
import logging

import flet as ft

from components.primitives.empty import Empty

from components.app.room import RoomPane
from contexts.room import RoomContext, RoomContextValue
from contexts.user import UserContext
from state.room_state import RoomState

logger = logging.getLogger(__name__)


@ft.component
def AppPage() -> ft.Control:
	user_context = ft.use_context(UserContext)

	if user_context.user is None:
		logger.warning("no user in AppPage — Router should have guarded this")
		return Empty()

	room_state, _ = ft.use_state(RoomState(rooms=[]))

	open_room = ft.use_callback(
		lambda id, section: room_state.open_room(id, section),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	close_room = ft.use_callback(
		lambda: room_state.close_room(),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	refresh_rooms = ft.use_callback(
		lambda: room_state.refresh_rooms(),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
		],
	)

	room_context = ft.use_memo(
		lambda: RoomContextValue(
			room=room_state.room,
			rooms=room_state.rooms,
			open_section=room_state.open_section,
			refresh=refresh_rooms,
			open=open_room,
			close=close_room,
		),
		dependencies=[
			room_state.room,
			room_state.rooms,
			room_state.open_section,
			open_room,
			close_room,
		],
	)

	def _refresh() -> None:
		async def _do_refresh():
			logger.info(
				"loading rooms",
				extra={"user": user_context.user.id if user_context.user else None},
			)
			try:
				await room_context.refresh()
				logger.info(
					"rooms loaded",
					extra={"count": len(room_state.rooms)},
				)
			except Exception as e:
				logger.exception("failed to load rooms")

		asyncio.create_task(_do_refresh())

	ft.use_effect(_refresh, [])

	room_wrapped = RoomContext(
		value=room_context,
		callback=RoomPane,
	)

	return room_wrapped
