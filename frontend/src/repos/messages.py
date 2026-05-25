from models.message import Message


class MessagesRepository:
	async def get_messages(self) -> list[Message]:
		raise NotImplementedError
