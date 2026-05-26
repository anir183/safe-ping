from typing import override

from models.room import Room
from repos.rooms import RoomsRepository


class MockRoomRepository(RoomsRepository):
	_all_rooms = [
		Room(
			"1",
			"Tom's Room",
			"4",
			["1", "2", "3"],
			"https://picsum.photos/106",
		),
		Room(
			"2",
			"Bob's Room",
			"2",
			["2", "4"],
			"https://picsum.photos/107",
		),
		Room(
			"3",
			"Max's Room",
			"3",
			["4", "1", "5"],
			"https://picsum.photos/108",
		),
		Room(
			"4",
			"Alice's Room",
			"1",
			["4", "5"],
			"https://picsum.photos/109",
		),
		Room(
			"5",
			"Elise's Room",
			"5",
			["5", "1", "2", "4", "3"],
			"https://picsum.photos/110",
		),
	]

	@override
	async def get_rooms(self, user_id: str | None = None) -> list[Room]:
		if user_id is None:
			return list(self._all_rooms)
		return [
			r
			for r in self._all_rooms
			if user_id == r.owner_id or user_id in r.member_ids
		]
