from dataclasses import dataclass


@dataclass
class Room:
	id: int
	name: str
	owner_id: int
	member_ids: list[int]
