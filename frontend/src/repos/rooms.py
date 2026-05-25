from models.room import Room


class RoomsRepository:
	async def get_rooms(self) -> list[Room]:
		raise NotImplementedError
