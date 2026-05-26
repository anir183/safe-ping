import asyncio
from typing import override

from models.notes import Note
from repos.notes import NotesRepository


class MockNotesRepository(NotesRepository):
	_notes: dict[str, Note] = {
			"1": Note(
				"1", "1",
				"Room Notes",
				"Welcome to Tom's Room!\n\nThis is a shared workspace for the team.",
				"12 Sat 10:00",
				"12 Sat 10:00",
			),
			"2": Note(
				"2", "2",
				"Project Ideas",
				"Brainstorming session notes go here.",
				"12 Sat 12:00",
				"12 Sat 12:00",
			),
			"3": Note(
				"3", "3",
				"Meeting Minutes",
				"Max's room meeting notes.\n\nAgenda:\n1. Standup\n2. Planning\n3. Parking lot",
				"11 Sun 09:00",
				"11 Sun 09:00",
			),
			"4": Note(
				"4", "4",
				"Untitled Note",
				"Start writing...",
				"12 Sun 14:00",
				"12 Sun 14:00",
			),
			"5": Note(
				"5", "5",
				"Elise's Scratchpad",
				"Random thoughts and ideas.",
				"13 Sun 08:00",
				"13 Sun 08:00",
			),
		}

	@override
	async def get_note(self, room_id: str) -> Note | None:
		await asyncio.sleep(0.3)
		return self._notes.get(room_id)

	@override
	async def save_note(self, room_id: str, note: Note) -> None:
		await asyncio.sleep(0.1)
		self._notes[room_id] = note
