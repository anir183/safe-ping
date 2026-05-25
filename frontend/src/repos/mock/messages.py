import asyncio
from typing import override

from models.message import Message
from repos.messages import MessagesRepository


class MockMessagesRepository(MessagesRepository):
	@override
	async def get_messages(self) -> list[Message]:
		await asyncio.sleep(1)

		return [
			Message("1", "1", "Message from Alice", "12 Sat"),
			Message("2", "2", "Message from Bob", "12 Sat"),
			Message("3", "3", "Message from Max", "11 Sun"),
			Message("4", "4", "Message from Tom", "12 Sun"),
			Message("5", "5", "Message from Elise", "13 Sun"),
		]
