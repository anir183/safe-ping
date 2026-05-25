from dataclasses import dataclass


@dataclass
class Message:
	id: str
	sender_id: str
	content: str
	timestamp: str
