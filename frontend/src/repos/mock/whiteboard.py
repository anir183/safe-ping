import asyncio
from typing import override

from models.whiteboard import WhiteboardStroke
from repos.whiteboard import WhiteboardRepository


class MockWhiteboardRepository(WhiteboardRepository):
	_strokes: dict[str, list[WhiteboardStroke]] = {
			"1": [],
			"2": [],
			"3": [],
			"4": [],
			"5": [],
		}

	@override
	async def get_strokes(self, room_id: str) -> list[WhiteboardStroke]:
		await asyncio.sleep(0.3)
		return list(self._strokes.get(room_id, []))

	@override
	async def save_strokes(self, room_id: str, strokes: list[WhiteboardStroke]) -> None:
		await asyncio.sleep(0.1)
		self._strokes[room_id] = list(strokes)
