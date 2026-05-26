from models.room import Room


class RoomsRepository:
	async def get_rooms(self, user_id: str | None = None) -> list[Room]:
		raise NotImplementedError
