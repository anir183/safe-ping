import logging
from dataclasses import dataclass

import flet as ft

from constants.room import ROOM_SECTION_CHAT
from models.room import Room
from repos.mock.room import MockRoomRepository
from repos.rooms import RoomsRepository

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class RoomState:
	rooms: list[Room]
	room: Room | None = None

	open_section: str = ROOM_SECTION_CHAT
	repo: RoomsRepository = MockRoomRepository()

	async def refresh_rooms(self):
		self.rooms = await self.repo.get_rooms()

	def open_room(self, id: str | None, section: str | None) -> None:
		room = next(
			(r for r in self.rooms if r.id == id),
			None,
		)
		self.room = room
		self.open_section = section is not None and section or ROOM_SECTION_CHAT

		logger.info(
			"opened room",
			extra={
				"room": self.room,
				"open-section": self.open_section,
			},
		)

	def close_room(self) -> None:
		logger.info(
			"closing room",
			extra={
				"room": self.room,
			},
		)

		self.room = None
		self.open_section = ROOM_SECTION_CHAT
