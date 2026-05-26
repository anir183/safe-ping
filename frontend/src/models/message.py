from dataclasses import dataclass


@dataclass
class Message:
	id: str
	room_id: str
	sender_id: str
	content: str
	timestamp: str
