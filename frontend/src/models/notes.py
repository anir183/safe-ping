from dataclasses import dataclass


@dataclass
class Note:
	id: str
	room_id: str
	title: str
	content: str
	created_at: str
	updated_at: str
