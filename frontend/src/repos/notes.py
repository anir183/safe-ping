from models.notes import Note


class NotesRepository:
	async def get_note(self, room_id: str) -> Note | None:
		raise NotImplementedError

	async def save_note(self, room_id: str, note: Note) -> None:
		raise NotImplementedError
