from models.message import Message


class MessagesRepository:
	async def get_messages(self, room_id: str) -> list[Message]:
		raise NotImplementedError

	async def add_message(self, room_id: str, message: Message) -> None:
		raise NotImplementedError
