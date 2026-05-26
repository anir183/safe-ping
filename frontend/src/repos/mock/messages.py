import asyncio
from typing import override

from models.message import Message
from repos.messages import MessagesRepository


class MockMessagesRepository(MessagesRepository):
	_messages: dict[str, list[Message]] = {
		"1": [
			Message("1", "1", "4", "Hey Tom, welcome to the room!", "12 Sat"),
			Message("2", "1", "1", "Thanks Alice! Excited to be here.", "12 Sat"),
			Message("3", "1", "2", "Hey everyone, Bob here!", "12 Sat"),
		],
		"2": [
			Message("4", "2", "2", "Bob's room, Bob's rules!", "12 Sat"),
		],
		"3": [
			Message("5", "3", "3", "Welcome to Max's room folks!", "11 Sun"),
			Message("6", "3", "4", "Hey Max, thanks for the invite!", "11 Sun"),
			Message("7", "3", "1", "Love this place already!", "11 Sun"),
			Message("8", "3", "5", "Elise reporting for duty!", "11 Sun"),
		],
		"4": [
			Message("9", "4", "1", "Alice's humble abode. Make yourself at home!", "12 Sun"),
			Message("10", "4", "4", "Cozy vibes in here!", "12 Sun"),
		],
		"5": [
			Message("11", "5", "5", "Elise's grand room — all are welcome!", "13 Sun"),
			Message("12", "5", "1", "Hey Elise! Count me in.", "13 Sun"),
			Message("13", "5", "2", "Bob here, ready to chat!", "13 Sun"),
			Message("14", "5", "4", "Tom joining the party!", "13 Sun"),
			Message("15", "5", "3", "Max is here too!", "13 Sun"),
		],
	}

	@override
	async def get_messages(self, room_id: str) -> list[Message]:
		await asyncio.sleep(0.3)
		return list(self._messages.get(room_id, []))

	@override
	async def add_message(self, room_id: str, message: Message) -> None:
		await asyncio.sleep(0.1)
		if room_id not in self._messages:
			self._messages[room_id] = []
		self._messages[room_id].append(message)
