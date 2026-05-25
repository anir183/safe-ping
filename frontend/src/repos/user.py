from models.user import User


class UserRepository:
	async def get_users(self) -> list[User]:
		raise NotImplementedError
