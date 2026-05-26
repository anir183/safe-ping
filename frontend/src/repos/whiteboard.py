from models.whiteboard import WhiteboardStroke


class WhiteboardRepository:
	async def get_strokes(self, room_id: str) -> list[WhiteboardStroke]:
		raise NotImplementedError

	async def save_strokes(self, room_id: str, strokes: list[WhiteboardStroke]) -> None:
		raise NotImplementedError
