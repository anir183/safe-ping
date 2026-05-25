import logging
from dataclasses import dataclass

import flet as ft

from constants.room import ROOM_SECTION_CHAT

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class RoomState:
	room_id: str | None = None
	open_section: str = ROOM_SECTION_CHAT

	def open_room(self, id: str | None, section: str | None) -> None:
		self.room_id = id
		self.open_section = section is not None and section or ROOM_SECTION_CHAT

		logger.info(
			"opened room",
			extra={
				"room-id": self.room_id,
				"open-section": self.open_section,
			},
		)

	def close_room(self) -> None:
		logger.info(
			"closing room",
			extra={
				"room-id": self.room_id,
			},
		)

		self.room_id = None
		self.open_section = ROOM_SECTION_CHAT
