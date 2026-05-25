from dataclasses import dataclass


@dataclass
class Room:
	id: str
	name: str
	owner_id: str
	member_ids: list[str]
	avatar: str
