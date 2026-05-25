import asyncio
from typing import override

from models.message import Message
from repos.messages import MessagesRepository


class MockMessagesRepository(MessagesRepository):
	@override
	async def get_messages(self) -> list[Message]:
		await asyncio.sleep(1)

		return [
			Message(1, 1, "Message from Alice", ""),
			Message(2, 2, "Message from Bob", ""),
			Message(3, 3, "Message from Max", ""),
			Message(4, 4, "Message from Tom", ""),
			Message(5, 5, "Message from Elise", ""),
		]
