import asyncio
from typing import override

from models.room import Room
from repos.rooms import RoomsRepository


class MockRoomRepository(RoomsRepository):
	@override
	async def get_rooms(self) -> list[Room]:
		await asyncio.sleep(1)

		return [
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
