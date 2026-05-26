from dataclasses import dataclass


@dataclass
class WhiteboardStroke:
	id: str
	room_id: str
	points: list[tuple[float, float]]
	color: str
	stroke_width: int
